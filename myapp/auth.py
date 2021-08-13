from flask import Blueprint, request
from flask import request, Blueprint, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import SQLAlchemy
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

db = SQLAlchemy()
bp = Blueprint("auth", __name__, url_prefix="/auth")


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)


def user_to_dict(user):
    return {"id": user.id, "username": user.username}


@bp.route("/users", methods=["GET", "POST"])
@jwt_required()
def users():
    if request.method == "GET":
        return jsonify([user_to_dict(u) for u in User.query.all()])
    if request.method == "POST":
        # ensure that requesting user is admin.
        # only admins can create new users.
        identity = get_jwt_identity()
        user = User.query.filter_by(username=identity).first()
        if not user or not user.is_admin:
            return "Must be admin to create new user.", 401
        if request.json is None:
            return "JSON body required.", 400
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username:
            return "'username' field required.", 400
        if not password:
            return "'password' field required.", 400
        user = User(username=username, password=password)
        user.password = pbkdf2_sha256.hash(user.password)
        db.session.add(user)
        db.session.commit()
        return "Ok", 200


@bp.route("/login", methods=["POST"])
def login():
    if request.json is None:
        return "JSON body required.", 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "Username not found.", 404
    pass_ok = password and pbkdf2_sha256.verify(password, user.password)
    if not pass_ok:
        return "Bad username or password.", 401

    access = create_access_token(identity=username)
    refresh = create_refresh_token(identity=username)
    return jsonify({"access": access, "refresh": refresh})


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({"access": access})


@bp.route("/self", methods=["GET"])
@jwt_required()
def self():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    return jsonify(user_to_dict(user))
