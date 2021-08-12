from myapp import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_app(app):
    assert app.testing


def test_client(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"