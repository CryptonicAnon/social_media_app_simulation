#from command line run 'python3 -m flask run --debug' then access http://127.0.0.1:5000
#from WSL 'flask run host=0.0.0.0'
#will have to create individual format files to design layout for endpoint (or could realistically make em all look the same)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, initialize  # Import models and initialize function

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except User.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    initialize()

@app.route("/")
def home():
    return render_template('landing_login_page.html')

@app.route("/feed")
@login_required
def feed():
    return render_template('feed.html')

@app.route("/inbox")
@login_required
def inbox():
    return render_template('inbox.html', messages=[])

@app.route("/notifications")
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/submit_message', methods=['POST'])
@login_required
def submit_message():
    message = request.form.get('send_message')
    messages.append(message)
    return redirect(url_for('feed'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = User.get(User.username == username)
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('feed'))
            else:
                flash("Invalid password", "error")
        except User.DoesNotExist:
            flash("Invalid username", "error")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    initialize()  # Initialize the database
    app.run(debug=True)