import pytest
from flask import url_for
from myapp import create_app
from myapp import myblueprint


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SERVER_NAME": 'localhost',  # to enable url_for
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        }
    )

    # create db tables for all models declared in blueprints
    with app.app_context():
        myblueprint.db.create_all()

    yield app


@pytest.fixture
def client(app):
    test_client = app.test_client()
    # for convenience, attach a url_for function to the client that already has the app_context
    def uf(url_name):
        with app.app_context():
            return url_for(url_name)
    test_client.url_for = uf
    return test_client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()