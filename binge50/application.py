# dependencies
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_jsglue import JSGlue
import requests
from bs4 import BeautifulSoup
from peewee import *
from playhouse.shortcuts import model_to_dict

# configure application
app = Flask(__name__)
jsglue = JSGlue(app)

# configure database
db = PostgresqlDatabase(
    "pantry",
    user="ubuntu",
    password="pantry",
    host="localhost",
)

# configure data model
class BaseModel(Model):
    class Meta:
        database = db
    
class TVShow(BaseModel):
    imdb_id = TextField()
    name = TextField(unique=True)
    rating = FloatField()
    vote = TextField()
    trailer = TextField(null=True)
    tomato = IntegerField(null=True)
    tomato_payload = TextField(null=True)
    metascore = IntegerField(null=True)
    metascore_payload = TextField(null=True)
    
    class Meta:
        db_table = "tvshows"
    
# create table, one time use only
db.connect()
TVShow.create_table(TVShow)
db.close()

# configure routing
# display homepage
@app.route("/")
def index():
    
    tvshows = []
    for tvshow in TVShow.select().limit(10):
        tvshows.append(model_to_dict(tvshow))

    return render_template("index.html", tvshows=tvshows)

# retrieve 15 of the most recent IMDB top250 tv shows
@app.route("/json")
def json():
    
    tvshows = []
    for tvshow in TVShow.select():
        tvshows.append(model_to_dict(tvshow))
    
    # export show info from database in JSON format
    return jsonify(tvshows)
    
# update imdb, tomatometer, and metascore for each tv show
@app.route("/update")
def update():
    
    for tvshow in TVShow.select():
        
        # retrieve imdb rating
        imdb = requests.get("http://www.imdb.com/title/" + tvshow.imdb_id)
        imdb_soup = BeautifulSoup(imdb.content, "html.parser")
        imdb_rating = imdb_soup.find("div", class_="ratingValue").span.string.strip()
        imdb_vote = imdb_soup.find("div", class_="imdbRating").find("span", class_="small").string.strip()
        
        # retrieve tomatometer
        tomato = requests.get("https://www.rottentomatoes.com/tv/" + tvshow.tomato_payload)
        tomato_soup = BeautifulSoup(tomato.content, "html.parser")
        tomatometer = tomato_soup.find("span", class_="meter-value").span.string.strip()
        
        # retrieve metascore
        metacritic = requests.get("http://www.metacritic.com/tv/" + tvshow.metascore_payload, headers={'User-Agent': 'Chrome/57.0.2987.133'})
        metacritic_soup = BeautifulSoup(metacritic.content, "html.parser")
        try:
            metascore = metacritic_soup.find("div", class_="metascore_w xlarge tvshow positive").span.string.strip()
        except AttributeError:
            metascore = 0
            
        # update database
        q = TVShow.update(rating=imdb_rating, vote=imdb_vote, tomato=tomatometer, metascore=metascore).where(TVShow.name == tvshow.name)
        q.execute()
        
    return redirect(url_for("index"))
        
    
# fetch 15 of the most recent IMDB top250 tv shows 
@app.route("/fetch_imdb")
def fetch_imdb():

    # fetch IMDB top-rated tv shows sorted by release date
    # to be included on the list, a series or mini series must receive ratings from at least 5000 users
    # a TV series must also have aired at least 5 episodes
    imdb = requests.get("http://www.imdb.com/chart/toptv/?sort=us")
    
    # make IMDB soup
    imdb_soup = BeautifulSoup(imdb.content, "html.parser")
    
    # sift out links to 10 of the most recent top-rated tv shows
    imdb_links = imdb_soup.find_all("td", class_="titleColumn", limit=15)
        
    # extract imdb title id from each url
    imdb_ids = []
    for link in imdb_links:
        url = link.a["href"]
        start = url.find("tt")
        end = url.find("/", start)
        imdb_ids.append(url[start:end])
        
    # extract show titles and ratings using title ids
    for id_ in imdb_ids:    
        imdb_title = requests.get("http://www.imdb.com/title/" + id_)
        imdb_title_soup = BeautifulSoup(imdb_title.content, "html.parser")
        imdb_title_name = imdb_title_soup.find("div", class_="title_wrapper").h1.string.strip()
        imdb_title_rating = imdb_title_soup.find("div", class_="ratingValue").span.string.strip()
        imdb_title_vote = imdb_title_soup.find("div", class_="imdbRating").find("span", class_="small").string.strip()
        
        # insert show info into database using peewee, update show info if already exists
        db.connect()
        try:
            TVShow.create(name=imdb_title_name, rating=imdb_title_rating, vote=imdb_title_vote, imdb_id=id_)
        except IntegrityError:
            db.rollback()
            q = TVShow.update(rating=imdb_title_rating, vote=imdb_title_vote).where(TVShow.name == imdb_title_name)
            q.execute()
        db.close()
    
    # redirect to home page
    return redirect(url_for("index"))
    
# fetch rotten tomato ratings for each tv show
@app.route("/fetch_tomato")
def fetch_tomato():
    
    for tvshow in TVShow.select():
        
        # look up tv show on Rotten Tomatoes
        if ":" in tvshow.name:
            start = tvshow.name.find(":")
            payload = tvshow.name[:start].replace(" ", "_")
        else:
            payload = tvshow.name.replace(" ", "_")
        tomato = requests.get("https://www.rottentomatoes.com/tv/" + payload)
        tomato_soup = BeautifulSoup(tomato.content, "html.parser")
        
        # extract Tomatometer score
        try:
            tomatometer = tomato_soup.find("span", class_="meter-value").span.string.strip()
        except AttributeError:
            tomatometer = 0
        
        # write tomatometer score to corresponding tv show in the database
        q = TVShow.update(tomato=tomatometer, tomato_payload=payload).where(TVShow.name == tvshow.name)
        q.execute()
    
    return redirect(url_for("index"))
    
# fetch metacritic scores for each tv show
@app.route("/fetch_metacritic")
def fetch_metacritic():
    
    for tvshow in TVShow.select():
        
        # look up tv show on Metacritic
        if ":" in tvshow.name:
            start = tvshow.name.find(":")
            payload = tvshow.name[:start].replace(" ", "-").lower()
        else:
            payload = tvshow.name.replace(" ", "-").lower()
        metacritic = requests.get("http://www.metacritic.com/tv/" + payload, headers={'User-Agent': 'Chrome/57.0.2987.133'})
        metacritic_soup = BeautifulSoup(metacritic.content, "html.parser")
        
        # extract Metascore
        try:
            metascore = metacritic_soup.find("div", class_="metascore_w xlarge tvshow positive").span.string.strip()
        # write 0 if no metascore yet
        except AttributeError:
            metascore = 0
        
        # write Metascore to database
        q = TVShow.update(metascore=metascore, metascore_payload=payload).where(TVShow.name == tvshow.name)
        q.execute()
        
    return redirect(url_for("index"))
    
# fetch youtube trailer id for each tv show using Duckduckgo api
@app.route("/fetch_trailer")
def fetch_trailer():
    
    # retrieve tv shows titles from the database
    for tvshow in TVShow.select():
        
        # look up tv show trailer on duckduckgo
        payload = {"q": tvshow.name + " tv offical trailer"}
        trailer = requests.get("https://duckduckgo.com/html/", params = payload)
        trailer_soup = BeautifulSoup(trailer.content, "html.parser")
        
        # extract 3 trailer url canditates from each search query
        trailer_urls = [url.string.strip() for url in trailer_soup.find_all("a", class_="result__url", limit=10)]
        
        # identify youtube trailer id from the candidates
        for trailer_url in trailer_urls:
            if "youtube.com/watch?v=" in trailer_url:
                start = trailer_url.find("=")
                youtube_id = trailer_url[start + 1:]
                
                # write youtube trailer id to corresponding tv show in the database
                q = TVShow.update(trailer=youtube_id).where(TVShow.name == tvshow.name)
                q.execute()
                
                # ensure only one youtube candidate is selected from each query
                break
            
    # redirect to home page
    return redirect(url_for("index"))