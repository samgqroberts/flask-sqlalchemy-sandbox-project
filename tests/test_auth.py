from flask_jwt_extended.utils import create_access_token, decode_token
from myapp.auth import User, db
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from flask_jwt_extended import create_refresh_token


def test_auth_roundtrip(client):
    """Test the integration of multiple auth-related endpoints"""

    res = client.post(
        client.url_for("auth.users"), json={"username": "user1", "password": "pw"}
    )
    assert res.status_code == 200
    assert res.data == b"Ok"

    res = client.post(
        client.url_for("auth.login"), json={"username": "user1", "password": "pw"}
    )
    assert res.status_code == 200
    res_json = res.get_json()
    access = res_json["access"]
    refresh = res_json["refresh"]
    assert access
    assert refresh

    res = client.get(
        client.url_for("auth.self"), headers=[("Authorization", f"Bearer {access}")]
    )
    assert res.status_code == 200
    assert res.get_json() == {"id": 1, "username": "user1"}


def test_get_users(app, client):
    res = client.get(client.url_for("auth.users"))
    assert res.status_code == 200
    assert res.get_json() == []

    with app.app_context():
        u1 = User(username="u1", password="pw1")
        u2 = User(username="u2", password="pw2")
        db.session.add_all([u1, u2])
        db.session.commit()
    res = client.get(client.url_for("auth.users"))
    assert res.status_code == 200
    assert res.get_json() == [{"id": 1, "username": "u1"}, {"id": 2, "username": "u2"}]


def test_add_user(app, client):
    res = client.post(client.url_for("auth.users"))
    assert res.status_code == 400
    assert res.data == b"JSON body required."

    res = client.post(client.url_for("auth.users"), json={})
    assert res.status_code == 400
    assert res.data == b"'username' field required."

    un = "u1"
    res = client.post(client.url_for("auth.users"), json={"username": un})
    assert res.status_code == 400
    assert res.data == b"'password' field required."

    pw = "pw1"
    res = client.post(
        client.url_for("auth.users"), json={"username": un, "password": pw}
    )
    assert res.status_code == 200
    assert res.data == b"Ok", 200

    with app.app_context():
        user = User.query.one()
        assert user.username == un
        # assert that the password got hashed as it got stored
        assert user.password != pw
        assert pbkdf2_sha256.verify(pw, user.password)


def test_login(app, client):
    with app.app_context():
        un = "u1"
        pw = "pw1"
        hashed_pw = pbkdf2_sha256.hash(pw)
        u1 = User(username=un, password=hashed_pw)
        db.session.add(u1)
        db.session.commit()

    res = client.post(client.url_for("auth.login"))
    assert res.status_code == 400
    assert res.data == b"JSON body required."

    res = client.post(client.url_for("auth.login"), json={})
    assert res.status_code == 404
    assert res.data == b"Username not found."

    res = client.post(client.url_for("auth.login"), json={"username": "nada"})
    assert res.status_code == 404
    assert res.data == b"Username not found."

    res = client.post(client.url_for("auth.login"), json={"username": un})
    assert res.status_code == 401
    assert res.data == b"Bad username or password."

    res = client.post(
        client.url_for("auth.login"), json={"username": un, "password": "nada"}
    )
    assert res.status_code == 401
    assert res.data == b"Bad username or password."

    res = client.post(
        client.url_for("auth.login"), json={"username": un, "password": pw}
    )
    assert res.status_code == 200
    res_json = res.get_json()
    assert res_json["access"]
    assert res_json["refresh"]


def test_refresh(app, client):
    un = "u1"
    with app.app_context():
        user = User(username=un, password="whatever")
        db.session.add(user)
        db.session.commit()
        refresh_token = create_refresh_token(un)

    res = client.post(client.url_for("auth.refresh"))
    assert res.status_code == 401
    assert res.get_json() == {"msg": "Missing Authorization Header"}

    res = client.post(
        client.url_for("auth.refresh"), headers=[("Authorization", f"Bearer nada")]
    )
    assert res.status_code == 422
    assert res.get_json() == {"msg": "Not enough segments"}

    res = client.post(
        client.url_for("auth.refresh"),
        headers=[("Authorization", f"Bearer {refresh_token}")],
    )
    assert res.status_code == 200
    access = res.get_json()["access"]
    assert access

    with app.app_context():
        # sub = "subject"
        assert decode_token(access)["sub"] == un


def test_self(app, client):
    un = "u1"
    with app.app_context():
        user = User(username=un, password="whatever")
        db.session.add(user)
        db.session.commit()
        access = create_access_token(un)

    res = client.get(client.url_for("auth.self"))
    assert res.status_code == 401
    assert res.get_json() == {"msg": "Missing Authorization Header"}

    res = client.get(
        client.url_for("auth.self"), headers=[("Authorization", f"Bearer nada")]
    )
    assert res.status_code == 422
    assert res.get_json() == {"msg": "Not enough segments"}

    res = client.get(
        client.url_for("auth.self"), headers=[("Authorization", f"Bearer {access}")]
    )
    assert res.status_code == 200
    assert res.get_json() == {"id": 1, "username": un}
