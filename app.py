#from command line run 'python3 -m flask run' then access http://127.0.0.1:5000
#will have to create individual format files to design layout for endpoint (or could realistically make em all look the same)
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/inbox")
def inbox():
    return render_template('inbox.html')

@app.route("/notifications")
def newsfeed():
    return render_template('notifications.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)