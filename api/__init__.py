from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    ENV = 'dev'

    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://aj:asdfasdf@localhost/battledb'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        ma.init_app(app)

        from api.Blog.blog_routes import blogs
        app.register_blueprint(blogs)

        return app
