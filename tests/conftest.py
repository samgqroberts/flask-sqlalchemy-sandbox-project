import pytest
from flask import url_for
from myapp import create_app, db
from myapp.db import (
    DEV_DB_USER,
    DEV_DB_PASSWORD,
    DEV_DB_HOST,
    DEV_DB_PORT,
    DEV_DB_CHARSET,
)

DB_NAME = "myapp_test"


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SERVER_NAME": "localhost",  # to enable url_for
            "SQLALCHEMY_DATABASE_URI": f"mysql+pymysql://{DEV_DB_USER}:{DEV_DB_PASSWORD}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DB_NAME}?charset={DEV_DB_CHARSET}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    db.drop_database(DB_NAME)
    db.create_database(DB_NAME)
    db.create_all_tables(app)

    yield app

    db.drop_database(DB_NAME)


@pytest.fixture
def client(app):
    test_client = app.test_client()
    # for convenience, attach a url_for function to the client that already has the app_context
    def uf(url_name, **values):
        with app.app_context():
            return url_for(url_name, **values)

    test_client.url_for = uf
    return test_client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
