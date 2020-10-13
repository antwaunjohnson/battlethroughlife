from api import db 
from datetime import datetime
from api.Tags_Blog.tag_blog_table import tag_blog


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