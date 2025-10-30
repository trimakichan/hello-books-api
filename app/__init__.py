from flask import Flask
from .db import db, migrate
from .models import book
from .routes.book_routes import books_bp
from .routes.home import home_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings
        # That lets you create different versions of the app — for example:
        # a development app/a testing app/a production app
        # Each version can have different configurations (like database URL, debugging mode, etc.).
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(home_bp)
    app.register_blueprint(books_bp)

    return app