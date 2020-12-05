import click
from flask.cli import with_appcontext
from .__init__ import db
from .Blog import Blog
from .User import User, OAuth


@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()
    db.session.commit()
    print("Database tables created")


def shell_context_processor():
    return{"db": db, "Blog": Blog, "User": User, "OAuth": OAuth}