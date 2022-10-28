from app.db import db
import bleach
from markdown import markdown
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.String(100))
    url = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    article_published = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    published = db.Column(db.Boolean, default=False)

    def format_date(self):
        string = self.article_published.strftime("%d-%m-%Y")
        return string

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(
        markdown(value, output_format='html'),
        tags=allowed_tags, strip=True))

    def __repr__(self):
        return f'Title {self.title}'

db.event.listen(Post.content, 'set', Post.on_changed_body)