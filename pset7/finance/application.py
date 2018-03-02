from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        flash("Logged in.")
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # clear pre-existing user_id
    session.clear()
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure proper usage for username
        if not request.form.get("username"):
            return apology("Missing username!")
            
        if (request.form.get("username")).isalnum() == False:
            return apology("Username must only consist of letters or numbers")
            
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password!")
        
        # ensure password confirmation was submitted    
        elif not request.form.get("passconfirm"):
            return apology("Missing password confirmation!")
            
        # ensure password matches confirmation
        elif request.form.get("password") != request.form.get("passconfirm"):
            return apology("Password confirmation does not match, please try again!")
            
        # encrypt password as hash
        hash = pwd_context.encrypt(request.form.get("password"))
        
        # insert user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
        
        # ensure user was properly inserted into database
        if result == None:
            return apology("Unable to register, please try again!")
            
        # store user id in session
        session["user_id"] = result
        
        # redirect registered user to home page
        flash("Registered.")
        return redirect(url_for("index"))
    
    # if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure proper usage for stock symbol
        if not request.form.get("symbol"):
            return apology("Missing stock symbol!")

        elif (request.form.get("symbol")).isalpha() == False:
            return apology("Invalid stock symbol, please try again!")
            
        # look up stock quote
        quote = lookup(request.form.get("symbol"))
        
        # ensure stock symbol provided is valid
        if quote == None:
            return apology("Invalid stock symbol, please try again!")
        
        # redirect user to quoted page
        flash("Quote success.")
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])
    
    # if user reacher route via GET (as by clicking a lnk or via redirect)
    else:
        return render_template("quote.html")
    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure proper usage for stock symbol
        if not request.form.get("symbol"):
            return apology("Missing stock symbol!")
            
        elif (request.form.get("symbol")).isalpha() == False:
            return apology("Invalid stock symbol, please try again!")
            
        # ensure proper usage for number of shares
        if not request.form.get("quantity"):
            return apology("Missing number of shares!")
            
        elif (request.form.get("quantity")).isnumeric() == False:
            return apology("Number of shares must be a positive integer, please try again!")
            
        elif float(request.form.get("quantity")) <= 0:
            return apology("Number of shares must be a positive integer, please try again!")
            
        elif hasdecimal(float(request.form.get("quantity"))):
            return apology("Number of shares must be a positive integer, please try again!")
            
        # look up stock quote
        quote = lookup(request.form.get("symbol"))
        
        # ensure stock symbol is valid
        if quote == None:
            return apology("Invalid stock symbol, please try again!")
            
        # retrieve user information
        user = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        
        # ensure user has sufficient balance to complete purchase
        buy_total = float(quote["price"]) * float(request.form.get("quantity"))
            
        if buy_total > balance[0]["cash"]:
            return apology("Insufficient funds to complete transaction.")
            
        # insert transaction into records
        records_result = db.execute("INSERT INTO records (user, symbol, quantity, price) VALUES(:user, :symbol, :quantity, :price)", user=user[0]["username"], symbol=quote["symbol"], quantity=request.form.get("quantity"), price=quote["price"])
        
        # ensure purchase was properly inserted into records
        if records_result == None:
            return apology("Unable to complete transaction, please try again!")
        
        # update user's cash balance
        users_result = db.execute("UPDATE users SET cash = cash - :total WHERE id = :id", total=buy_total, id=session["user_id"])
        
        # ensure balance was properly updated
        if users_result == None:
            return apology("Unable to update cash balance, you are screwed!")
            
        # update user's stocks overview
        stocks_result = db.execute("SELECT quantity FROM stocks WHERE user = :user AND symbol = :symbol", user=user[0]["username"], symbol=quote["symbol"])
        
        if stocks_result == []:   
            stock_result = db.execute("INSERT INTO stocks (user, symbol, quantity) VALUES(:user, :symbol, :quantity)", user=user[0]["username"], symbol=quote["symbol"], quantity=request.form.get("quantity"))
        
        else:
            stock_result = db.execute("UPDATE stocks SET quantity = quantity + :share WHERE user = :user AND symbol = :symbol", share=request.form.get("quantity"), user=user[0]["username"], symbol=quote["symbol"])
            
        # ensure update to stocks overview was successful
        if stock_result == None:
            return apology("Unable to update stocks overview, you are so screwed!")
        
        # redirect user to home page after purchase
        flash("Stock purchased.")
        return redirect(url_for("index"))
    
     # if user reacher route via GET (as by clicking a lnk or via redirect)
    else:
        return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure proper usage for stock symbol
        if not request.form.get("symbol"):
            return apology("Missing stock symbol!")

        elif (request.form.get("symbol")).isalpha() == False:
            return apology("Invalid stock symbol, please try again!")
            
        # ensure proper usage of number of shares
        if not request.form.get("quantity"):
            return apology("Missing number of shares!")
            
        elif (request.form.get("quantity")).isnumeric() == False:
            return apology("Number of shares must be a positive integer, please try again!")
            
        elif float(request.form.get("quantity")) <= 0:
            return apology("Number of shares must be a positive integer, please try again!")
            
        elif hasdecimal(float(request.form.get("quantity"))):
            return apology("Number of shares must be a positive integer, please try again!")        
            
        # look up stock quote
        quote = lookup(request.form.get("symbol"))
        
        # ensure stock symbol is valid
        if quote == None:
            return apology("Invalid stock symbol, please try again!")
            
        # retrieve user information
        user = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        stocks_result = db.execute("SELECT * FROM stocks WHERE user = :user AND symbol = :symbol", user=user[0]["username"], symbol=request.form.get("symbol"))
        
        # ensure user owns the stock to sell
        if stocks_result == []:
            return apology("You are trying to sell a stock that you do not own, please double check your stock symbol!")
            
        # ensure user has enough stock to sell
        if stocks_result[0]["quantity"] < float(request.form.get("quantity")):
            return apology("You do not possess enough shares to complete the transaction.")
            
        # insert transaction into records
        records_result = db.execute("INSERT INTO records (user, symbol, quantity, price) VALUES(:user, :symbol, :quantity, :price)", user=user[0]["username"], symbol=quote["symbol"], quantity= "-" + request.form.get("quantity"), price=quote["price"])
        
        # ensure transaction was properly inserted into records
        if records_result == None:
            return apology("Unable to complete tranasction, please try again!")
            
        # update user's cash balance
        sell_total = float(quote["price"]) * float(request.form.get("quantity"))
        users_result = db.execute("UPDATE users SET cash = cash + :total WHERE id = :id", total=sell_total, id=session["user_id"])
        
        # ensure balance was properly updated
        if users_result == None:
            return apology("Unable to update cash balance, you are screwed!")
            
        # update user's stocks overview
        if stocks_result[0]["quantity"] > float(request.form.get("quantity")):
            stock_result = db.execute("UPDATE stocks SET quantity = quantity - :share WHERE user = :user AND symbol = :symbol", share=request.form.get("quantity"), user=user[0]["username"], symbol=quote["symbol"])
            
        else:
            stock_result = db.execute("DELETE FROM stocks WHERE user = :user AND symbol = :symbol", user=user[0]["username"], symbol=quote["symbol"])
            
        # ensure update to stocks overview was successful
        if stock_result == None:
            return apology("Unable to complete transaction, please try again later!")
        
        # redirect user to home page after transaction
        flash("Stock sold.")
        return redirect(url_for("index"))
    
    # if user reacher route via GET (as by clicking a lnk or via redirect)
    return render_template("sell.html")
    
@app.route("/")
@login_required
def index():
    
    # retrieve user information
    user = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    stocks = db.execute("SELECT * FROM stocks WHERE user = :user", user=user[0]["username"])
    
    # append names, current prices, and total values to stocks
    stocks_value = 0
    
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = float(stock["price"] * stock["quantity"])
    
        # stocks value counter
        stocks_value += stock["total"]
        
        # stylize output with usd
        stock["total"] = usd(stock["total"])
        stock["price"] = usd(stock["price"])
        
    # determine remaining cash for current user
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    
    # determine total asset for current user
    user_total = stocks_value + cash[0]["cash"]
    
    # display user's stocks overview
    return render_template("index.html", stocks=stocks, cash=usd(cash[0]["cash"]), total=usd(user_total))
    
@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    # retrieve user information
    user = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    records = db.execute("SELECT * FROM records WHERE user = :user", user=user[0]["username"])
    
    if records == None:
        return apology("Something has gone wrong, please try again later!")
    
    # stylize output with usd
    for record in records:
        record["price"] = usd(record["price"])
    
    return render_template("history.html", records=records)

@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    """Reset user password."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure proper usage
        if not request.form.get("old_pass"):
            return apology("Please provide original password.")
            
        if not request.form.get("new_pass"):
            return apology("Please provide new password.")
            
        if not request.form.get("confirm_new_pass"):
            return apology("Please confirm new password.")
            
        if request.form.get("new_pass") != request.form.get("confirm_new_pass"):
            return apology("New passwords do not match, please try again!")
            
        # encrypt new password
        hash = pwd_context.encrypt(request.form.get("new_pass"))
        
        # reset user password
        result = db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id=session["user_id"])
        
        # redirect user to home page
        flash("Password reset.")
        return redirect(url_for("index"))
        
    # if user reacher route via GET (as by clicking a lnk or via redirect)
    else:    
        return render_template("reset.html")