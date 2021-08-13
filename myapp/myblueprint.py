from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
blueprint = Blueprint('myblueprint', __name__)


def thing_to_dict(thing):
    return {'id': thing.id, 'name': thing.name}


class Thing(db.Model):
    __tablename__ = 'thing'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


@blueprint.route("/things", methods=("GET", "POST"))
def things():
    if request.method == "GET":
        things = Thing.query.all()
        return jsonify([thing_to_dict(t) for t in things])
    if request.method == "POST":
        data = request.get_json()
        newThing = Thing(name=data['name'])
        db.session.add(newThing)
        db.session.commit()
        return 'Ok', 200


@blueprint.route("/things/<int:id>", methods=("GET", "PUT", "DELETE"))
def thing(id):
    thing = Thing.query.get_or_404(id)
    if request.method == "GET":
        return jsonify(thing_to_dict(thing))
    if request.method == "PUT":
        data = request.get_json()
        if not data or 'name' not in data:
            return 'Provided json body needs a "name" field.', 400
        thing.name = data['name']
        db.session.commit()
        return 'Ok', 200
    if request.method == "DELETE":
        db.session.delete(thing)
        db.session.commit()
        return 'Ok', 200
