import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # load positive words into memory
        self.positives = set()
        pos_file = open(positives, "r")
        for pos_line in pos_file:
            if (pos_line.startswith(";") == False):
                self.positives.add(pos_line.strip())
        pos_file.close()
        
        # load negative words into memory
        self.negatives = set()
        neg_file = open(negatives, "r")
        for neg_line in neg_file:
            if (neg_line.startswith(";") == False):
                self.negatives.add(neg_line.strip())
        neg_file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # tokenize text
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(str(text))
        
        # initiate sentiment score
        sentiment = 0
        
        # iterate over text tokens
        for token in tokens:
            # plus one sentiment score if found in positive set
            if token.lower() in self.positives:
                sentiment += 1
            # minus one sentiment score if found in negative set
            elif token.lower() in self.negatives:
                sentiment -= 1
        
        # return sentiment score
        return sentiment
