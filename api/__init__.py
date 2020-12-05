from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from .config import Config
from .cli import create_db, shell_context_processor

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()


def create_app():
    app=Flask(__name__)

    app.config.from_object(Config)
   
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    from api.Blog.blog_routes import blogs
    app.register_blueprint(blogs)

    from api.User.user_model import User

    from api.Oauth.google import google_blueprint
    app.register_blueprint(google_blueprint)

    app.cli.add_command(create_db)
    app.shell_context_processors.append(shell_context_processor)
    

    return app