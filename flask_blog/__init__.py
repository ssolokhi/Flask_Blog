from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config

database = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object(Config)
    
    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_blog.main.routes import main
    app.register_blueprint(main)
    from flask_blog.users.routes import users
    app.register_blueprint(users)
    from flask_blog.posts.routes import posts
    app.register_blueprint(posts)
    from flask_blog.errors.handlers import errors
    app.register_blueprint(errors)    
    return app