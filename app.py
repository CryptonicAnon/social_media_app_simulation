#to test on wsl: flask run --host=0.0.0.0
from flask import (Flask, g, render_template, render_template, request, redirect, url_for, flash, session,
                  abort)
from flask_bcrypt import (Bcrypt, check_password_hash)
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models
from models import User, initialize

messages = []

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
    return render_template('inbox.html', messages=messages)

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

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            password2=form.password2.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    models.initialize()
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