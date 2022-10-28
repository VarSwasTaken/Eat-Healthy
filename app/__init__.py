# from app import routes
from app.main import bp as main_bp
from app.auth import bp as auth_bp
from flask import Flask
from config import Config

from app.db import db
from flask_migrate import Migrate

from flask_pagedown import PageDown

from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

pagedown = PageDown(app)

login = LoginManager(app)
login.login_view = 'auth.login'

app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(main_bp)
