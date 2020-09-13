from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

@app.route('/')
def new_project():
    return 'This will be my new blog project'


if __name__ == '__main__':
    app.run(debug=True)
