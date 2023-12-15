from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_blog.models import User, Post
from flask_blog import app, database, bcrypt
from secrets import token_hex
from os import path
from PIL import Image

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        database.session.add(user) 
        database.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Unsuccessififul login attempt!', 'danger')
    return render_template('login.html', title = 'Log In', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_image(form_image):
    random_hex = token_hex(8)
    _, file_extension = path.splitext(form_image.filename)
    image_filename = ''.join([random_hex, file_extension])
    image_path = path.join(app.root_path, 'static', 'profile_images', image_filename)
    output_size_pixels = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size_pixels) # resize image to avoid costly rendering
    i.save(image_path)
    return image_filename

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        database.session.commit()
        flash('Account information updated successfully!', 'success')
        return redirect(url_for('account')) # to avoid post-get-redirect pattern with next return
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = f'profile_images/{current_user.image_file}')
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)