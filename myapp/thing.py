from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema

db = SQLAlchemy()
bp = Blueprint("thing", __name__, url_prefix="/things")


class Thing(db.Model):
    __tablename__ = "thing"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


class ThingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Thing


@bp.route("/", methods=("GET", "POST"))
def things():
    if request.method == "GET":
        things = Thing.query.all()
        return jsonify([ThingSchema().dump(t) for t in things])
    if request.method == "POST":
        data = request.get_json()
        newThing = Thing(name=data["name"])
        db.session.add(newThing)
        db.session.commit()
        return "Ok", 200


@bp.route("/<int:id>", methods=("GET", "PUT", "DELETE"))
def thing(id):
    thing = Thing.query.get_or_404(id)
    if request.method == "GET":
        return jsonify(ThingSchema().dump(thing))
    if request.method == "PUT":
        data = request.get_json()
        if not data or "name" not in data:
            return 'Provided json body needs a "name" field.', 400
        thing.name = data["name"]
        db.session.commit()
        return "Ok", 200
    if request.method == "DELETE":
        db.session.delete(thing)
        db.session.commit()
        return "Ok", 200
