#from command line run 'python3 -m flask run --debug' then access http://127.0.0.1:5000
#from WSL 'flask run host=0.0.0.0'
#will have to create individual format files to design layout for endpoint (or could realistically make em all look the same)
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

messages = []
valid_username = "user"
valid_password = "pass"

@app.route("/")
def home():
    return render_template('landing_login_page.html')

@app.route("/feed")
def feed():
    return render_template('feed.html')

@app.route("/inbox")
def inbox():
    return render_template('inbox.html', messages=messages)

@app.route("/notifications")
def newsfeed():
    return render_template('notifications.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form.get('send_message')  # Get the submitted message
    messages.append(message)  # Store the message in the inbox
    return redirect(url_for('feed'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if credentials match
        if username == valid_username and password == valid_password:
            return redirect(url_for('feed'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))
    
    return render_template('login.html')  # Display login form if GET request

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove the session variable
    return redirect(url_for('landing_login_page'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)