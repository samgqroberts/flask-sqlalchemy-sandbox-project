from myapp import create_app


def test_app_fixture(app):
    assert not create_app().testing
    assert app.testing


def test_client(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"