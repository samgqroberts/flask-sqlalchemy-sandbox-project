from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    # create the base app
    app = Flask(__name__)

    # configure app, depending on whether this is a testing context
    if test_config is None:
        app.config.from_pyfile("../settings.cfg")
    else:
        app.config.from_mapping(test_config)

    # initialize and configure database connection
    db = SQLAlchemy(
        app=app,
        engine_options={
            "pool_pre_ping": True,
            "isolation_level": "READ UNCOMMITTED",
            "query_cache_size": 0,
        },
    )
    db.init_app(app)

    # initialize and configure JWT manager
    app.config["JWT_SECRET_KEY"] = "bf3c71e4-15dd-4679-b3e3-ce5f36fbd789"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=14)
    JWTManager(app)

    # incorporate all blueprints
    for module in get_all_blueprint_modules():
        app.register_blueprint(module.bp)
        module.db.init_app(app)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app


def get_all_blueprint_modules():
    from . import auth, thing

    return [auth, thing]
