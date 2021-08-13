import pytest
from flask import url_for
from myapp import create_app
from myapp import db

DB_USER="root"
DB_PASSWORD="12345"
DB_HOST="127.0.0.1"
DB_PORT="3308"
DB_NAME="myapp_test"
DB_CHARSET="utf8mb4"

@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SERVER_NAME": 'localhost',  # to enable url_for
            "SQLALCHEMY_DATABASE_URI":f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
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
    def uf(url_name):
        with app.app_context():
            return url_for(url_name)
    test_client.url_for = uf
    return test_client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()