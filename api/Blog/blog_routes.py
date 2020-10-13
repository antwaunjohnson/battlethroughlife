from flask import Blueprint, jsonify, request
from .blog_model import Blog
from api.Tag.tag_model import Tag
from api import db 
from api import ma

blogs = Blueprint('blogs', __name__)

class BlogSchema(ma.Schema):
    class Meta:
        fields = (id, 'title', 'content', 'featured_image', 'created_at')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

# Endpoint to create a new blog

@blogs.route('/add_blog', methods=['POST'])
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
@blogs.route('/blogs', methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)


# Endpoint for querying a single blog
@blogs.route('/blog/<id>', methods=["GET"])
def get_blog(id):
    blog = Blog.query.get(id)

    for tag in blog.tags:
        tag.append(tag)

    return blog_schema.jsonify(blog)


# Endpoint for updating a blog
@blogs.route('/update_blog/<id>', methods=["PUT"])
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
@blogs.route('/delete_blog/<id>', methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.get(id)
    title = request.json['title']

    blog.title = title

    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was succesfully deleted")