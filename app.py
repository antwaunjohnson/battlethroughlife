from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from os import environ


app = Flask(__name__)





ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'

    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



# Blog model for api


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.Text, unique=False)
    featured_image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __init__(self, id, title, content, featured_image, created_at):
        self.id = id
        self.title = title
        self.content = content
        self.featured_image = featured_image
        self.created_at = created_at

# Tag model 


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, id, name):
        self.id = id
        self.name = name

# Tag_blog table

tag_blog = db.Table('tag_blog',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True)
)

# Blog schema and routes for api

class BlogSchema(ma.Schema):
    class Meta:
        fields = (id, 'title', 'content', 'featured_image', 'created_at')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

# Endpoint to create a new blog

@app.route('/add_blog', methods=['POST'])
def add_blog():
    data = request.get_json()

    title = request.json['title']
    content = request.json['content']
    featured_image = request.json['featured_image']
    

    new_blog = Blog( title, content, featured_image)

    for tag in data['tags']:
        present_tag = Tag.query.filter_by(name=tag).first()
        if(present_tag):
            present_tag.blogs_associated.append(new_blog)
        else:
            new_tag=Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)

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

    for tag in blog.tags:
        tag.append(tag)

    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@app.route('/update_blog/<id>', methods=["PUT"])
def update_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']
    featured_image = request.json['featured_image']

    blog.title = title
    blog.content = content
    blog.featured_image = featured_image

    db.session.commit()
    return blog_schema.jsonify(blog)


#Endpoint for deleting a blog
@app.route('/delete_blog/<id>', methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']

    blog.title = title

    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was succesfully deleted")


# Tag model and foreing_key

if __name__ == '__main__':
    app.run(debug=True)