from app import app
from app.db import db
from app.models.user import User
from app.models.post import Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}