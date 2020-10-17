from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)


ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://aj:asdfasdf@localhost/battledb'
    
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



# Blog model for api


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.Text, unique=False)
   

    def __init__(self, title, content):
        self.title = title
        self.content = content

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

# Endpoint to create a new blog

@app.route('/add_blog', methods=['POST'])
def add_blog():
    title = request.json['title']
    content = request.json['content']

    new_blog = Blog(title, content)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)

    return blog_schema.jsonify(blog)


# Endpoint to query all blogs
@app.route('/blogs', methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


# Endpoint for querying a single blog
@app.route('/blog/<id>', methods=["GET"])
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@app.route('/update_blog/<id>', methods=["PUT"])
def update_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']

    blog.title = title
    blog.content = content

    db.session.commit()
    return blog_schema.jsonify(blog)


#Endpoint for deleting a blog
@app.route('/blog/<id>', methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']

    blog.title = title

    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was succesfully deleted")



if __name__ == '__main__':
    app.run(debug=True)