from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
blueprint = Blueprint('myblueprint', __name__)

@blueprint.route("/things", methods=("GET", "POST"))
def things():
    if request.method == "GET":
        things = [
            'response',
            'to',
            'GET',
            'request'
        ]
        return jsonify(things)
    if request.method == "POST":
        things = [
            'response',
            'to',
            'POST',
            'request'
        ]
        return jsonify(things)