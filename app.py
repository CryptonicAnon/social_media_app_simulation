from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import models
from models import User, Post, Like, Comment, Relationship, initialize  # Import models and initialize function
import peewee
#from models import User, Post, Relationship, initialize  # Import models and initialize function

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
dms = []


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

@app.route("/create_account")
def register():
    return render_template('register.html')

@app.route("/feed")
@login_required
def feed():
    posts = Post.select()  # Fetch all posts from the database
    return render_template('feed.html', posts=posts)

@app.route('/send_dm', methods=['POST'])
@login_required
def send_dm():
    dm = request.form.get('send_dm')
    dms.append(dm)
    return redirect(url_for('send_dm'))

@app.route("/inbox")
@login_required
def inbox():
    return render_template('inbox.html', dms=dms)

@app.route("/notifications")
@login_required
def notifications():
    return render_template('notifications.html')

# @app.route('/submit_message', methods=['POST'])
# @login_required
# def submit_message():
#     message = request.form.get('send_message')
#     messages.append(message)
#     return redirect(url_for('feed'))

@app.route('/submit_post', methods=['POST'])
@login_required
def create_post():
    user = current_user.username
    content = request.form.get('send_post')
    Post.create(user=user, content=content)
    return redirect(url_for('feed'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_or_none(User.username == username)  # Use get_or_none to avoid exceptions

        if user and user.password == password:  # Check hashed password
            login_user(user)  # Log the user in
            return redirect(url_for('feed'))  # Redirect to feed after successful login
        else:
            flash("Invalid username or password", "error")  # Flash error message

    return render_template('login.html')  # Render login page for GET requests

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            models.User.create_user(username, email, password, admin=False)
            flash("Account created successfully. Please log in.", "success")  # Flash success message
            return redirect(url_for('login'))  # Redirect to login after successful account creation
        except Exception as e:
            flash("Account creation failed: " + str(e), "error")  # Flash error message

    return render_template('register.html')  # Render registration page for GET requests

@app.route('/like')
@login_required
def like_post(id):
    post = Post.get_or_none(Post.id == id)
    if post:
        try:
            Like.create(user=current_user, post=post)
        except peewee.IntegrityError as err:
            # Like already exists, do nothing
            pass
    return redirect(url_for('feed'))

@app.route('/comment/', methods=['POST'])
@login_required
def comment_post(id):
    post = Post.get_or_none(Post.id == id)
    content = request.form.get('content')
    if post and content:
        Comment.create(user=current_user, post=post, content=content)
    return redirect(url_for('feed'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))  # Redirect to home after logout

if __name__ == '__main__':
    initialize()  # Initialize the database
    try:
        models.User.create_user(
            username='testuser',
            email='test@test.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)