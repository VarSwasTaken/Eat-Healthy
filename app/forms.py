# from calendar import day_abbr
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, url
# from flask_pagedown.fields import PageDownField
# from app.models.user import User

<<<<<<< HEAD
# class CreatePostForm(FlaskForm):
#     title = StringField('Post title', validators=[DataRequired()])
#     description = StringField('Description', validators=[DataRequired()])
#     url = StringField('URL', validators=[DataRequired()])
#     content = PageDownField('Post content', validators=[DataRequired()])
#     submit = SubmitField('add post')
=======
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
>>>>>>> bb1a71411e18f4fdd617de1d1e6938c869c4f323

