from calendar import day_abbr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class CreatePostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    content = PageDownField('Post content', validators=[DataRequired()])
    submit = SubmitField('add post')
