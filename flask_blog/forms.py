from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User
import email_validator

# Python classes automatically converted to HTML forms

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_field(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('User with this username already exists')
    
    def validate_field(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('User with this email already exists')
    
class LoginForm(FlaskForm):
    username = StringField('Username', 
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('log In')