import click
from flask import g
from .models import db

def get_db():
    if 'db' not in g:
        g.db = db.engine.connect()
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@click.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database initialization successful.")

def init_app(app):
    db.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
