from datetime import datetime
from api import db 
from api import ma

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # created_by = db.Column(db.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)