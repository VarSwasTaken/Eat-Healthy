from calendar import day_abbr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


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

