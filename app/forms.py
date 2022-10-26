from calendar import day_abbr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, url
from flask_pagedown.fields import PageDownField
from app.models.user import User

class CreatePostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    post = PageDownField('Post content', validators=[DataRequired()])
    submit = SubmitField('add post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username required"),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password required"),
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username required"),
        Length(min=3, message="Username must be atleast 3 characters long")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email required"),
        Email(message="Wrong email input")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password required"),
        Length(min=8, message="Password must be atleast 8 characters long"),
        Regexp('(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])', message="Password must contain atleast 1 lowercase, 1 uppercase & 1 digit")
    ])
    password2 = PasswordField(
        'Repeat Password', validators=[
            DataRequired(message="Field required"),
            EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('You already have an account.')