from flask import render_template, url_for, flash, redirect
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_blog import app

posts = [
    {
        'author': 'Bob',
        'title': 'Blog Post 1',
        'content': 'First post',
        'date': 'April 1, 2023'
    },
    {
        'author': 'Alice',
        'title': 'Blog Post 2',
        'content': 'Second post',
        'date': 'April 1, 2023'
    }
]

@app.route("/")
@app.route("/home") # alias
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Unsuccessififul login attempt!', 'danger')
    return render_template('login.html', title = 'Log In', form = form)
