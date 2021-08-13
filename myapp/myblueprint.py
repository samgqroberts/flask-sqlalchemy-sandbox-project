from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
blueprint = Blueprint('myblueprint', __name__)


class Thing(db.Model):
    __tablename__ = 'thing'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


@blueprint.route("/things", methods=("GET", "POST"))
def things():
    if request.method == "GET":
        things = Thing.query.all()
        return jsonify([{ 'id': t.id, 'name': t.name } for t in things])
    if request.method == "POST":
        data = request.get_json()
        newThing = Thing(name=data['name'])
        db.session.add(newThing)
        db.session.commit()
        return 'Ok', 200