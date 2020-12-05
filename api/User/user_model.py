from api import db, login_manager
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.collections import attribute_mapped_collection


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    blogs = db.relationship('Blog', backref='blog', lazy=True)


class OAuth(OAuthConsumerMixin, db.Model):
    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User,
        backref=db.backref(
            "oath",
            collection_class=attribute_mapped_collection("provider"),
            cascade="all, delete-orphan"
        )
    )

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
