from flask_blog import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
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
    date = database.Column(database.DateTime, nullable = False, default = datetime.utcnow) # not utcnow(), or the current time would be passed
    content = database.Column(database.Text, nullable = False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f'Post(\'{self.title}\', \'{self.date}\')'