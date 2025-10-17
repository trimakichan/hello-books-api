from flask import Flask
from .routes.book_routes import books_bp
from .routes.home import home_bp
# from .routes.hello_world_routes import hello_world_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(books_bp)
    # app.register_blueprint(hello_world_bp)

    return app