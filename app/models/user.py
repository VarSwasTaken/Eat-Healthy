from datetime import datetime
from app.db import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    account_created = db.Column(db.DateTime, default=datetime.utcnow())
    admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String())
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   
    def format_date(self):
        string = self.account_created.strftime("%d-%m-%Y")
        return string


@login.user_loader
def load_user(id):
    return User.query.get(int(id))