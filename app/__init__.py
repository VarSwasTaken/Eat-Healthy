from flask import Flask
from config import Config

from app.db import db
from flask_migrate import Migrate

from flask_pagedown import PageDown

from flask_migrate import Migrate
from flask_login import LoginManager

migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
pagedown = PageDown()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)

    pagedown.init_app(app)

    login.init_app(app)



    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    # from app import errors

    return app
