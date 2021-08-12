from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
blueprint = Blueprint('myblueprint', __name__)

@blueprint.route("/things", methods=("GET",))
def list_things():
    things = [
        'thing1',
        'thing2'
    ]
    return jsonify(things)