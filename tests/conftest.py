import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.book import Book
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    # when a request is finished, it will remove everything from the session. 
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    # app.app_context() lets SQLAlchemy and Flask know which app is active.
    with app.app_context():
        # creates all tables defined by your models in the test database.
        db.create_all()
        # gives the app to the test — this is where your actual test runs.
        yield app

    # this removes all tables so every test starts fresh.
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    # This creates a Flask test client, which allows you to simulate requests
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                    description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                        description="i luv 2 climb rocks")
    
    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()
    