#from command line run 'python3 -m flask run' then access http://127.0.0.1:5000
#will have to create individual format files to design layout for endpoint (or could realistically make em all look the same)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/inbox")
def inbox():
    return "This is your inbox"

@app.route("/news_feed")
def newsfeed():
    return "This is your news feed"