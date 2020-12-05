from flask import Blueprint, request, jsonify
from flask_login import login_required
from api import db 
from api import ma
from .blog_model import Blog


blogs = Blueprint('blogs', __name__)

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

@blogs.route('/add_blog', methods=['POST'])
@login_required
def add_blog():
    title = request.json['title']
    content = request.json['content']

    new_blog = Blog(title, content)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)

    return blog_schema.jsonify(blog)


# Endpoint to query all blogs
@blogs.route('/blogs', methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


# Endpoint for querying a single blog
@blogs.route('/blog/<id>', methods=["GET"])
@login_required
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@blogs.route('/update_blog/<id>', methods=["PUT"])
@login_required
def update_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']

    blog.title = title
    blog.content = content

    db.session.commit()
    return blog_schema.jsonify(blog)


#Endpoint for deleting a blog
@blogs.route('/blog/<id>', methods=["DELETE"])
@login_required
def delete_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']

    blog.title = title

    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was succesfully deleted")