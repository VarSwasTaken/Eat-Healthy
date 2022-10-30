from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, EqualTo
from flask_wtf.file import FileField
from flask_pagedown.fields import PageDownField
from app.models.user import User

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
    username = StringField('Username', validators=[
        Length(min=3, message="Username must be at least 3 characters long")
    ])
    password = PasswordField('New Password', validators=[
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp('(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])',
               message="Password must contain at least 1 lowercase, 1 uppercase & 1 digit")
    ])
    password2 = PasswordField('Repeat New Password', validators=[
            EqualTo('newPassword', message="Passwords must match")
        ])
    avatar = FileField('Profile Picture')
    submit = SubmitField('Submit changes')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user.username != username.data and user is not None:
            raise ValidationError('Username taken.')