from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from os import environ
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

database = SQLAlchemy(app)

class User(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(20), unique = True, nullable = False)
    email = database.Column(database.String(120), unique = True, nullable = False)
    image_file = database.Column(database.String(20), nullable = False, default = 'default.jpg')
    password = database.Column(database.String(60), nullable = False)
    posts = database.relationship('Post', backref = 'author', lazy = True) # additional query, not a column
    
    def __repr__(self):
        return f'User(\'{self.username}\', \'{self.email}\',\'{self.image_file}\')'

class Post(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(100), nullable = False)
    date = database.Column(database.Datetime, nullable = False, default=datetime.utcnow) # not utcnow(), or the current time would be passed
    content = database.Column(database.Text, nullable = False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f'Post(\'{self.title}\', \'{self.date}\')'

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

if __name__ == '__main__':
    app.run(debug = True)