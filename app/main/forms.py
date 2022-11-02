from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed
from flask_pagedown.fields import PageDownField
from app.models.user import User
import imghdr

class CreatePostForm(FlaskForm):
    title = StringField('Post title', validators=[
        DataRequired(message="Title required")
    ])
    description = StringField('Description', validators=[
        DataRequired(message="Description required")
    ])
    url = StringField('URL', validators=[DataRequired()])
    content = PageDownField('Post content', validators=[
        DataRequired(message="URL required")
    ])
    submit = SubmitField('Add post')

class ChangeCridentialsForm(FlaskForm):
    currentPassword = PasswordField('Current Password', validators=[
        DataRequired(message="Password required")
    ])
    username = StringField('Username', validators=[
        Optional(),
        Length(min=3, message="Username must be at least 3 characters long")
    ])
    password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp('(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])',
               message="Password must contain at least 1 lowercase, 1 uppercase & 1 digit")
    ])
    password2 = PasswordField('Repeat New Password', validators=[
        EqualTo('password', message="Passwords must match")
    ])
    avatar = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'gif', 'apng', 'webp', 'svg', 'jfif', 'jpeg'], 'Only images are allowed!')
    ])
    submit = SubmitField('Submit changes')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken.')
    
    def validate_image(self, avatar):
        header = avatar.stream.read(512)
        avatar.stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            raise ValidationError('Only images are allowed!')
        return '.' + (format if format != 'jpeg' else 'jpg')

    