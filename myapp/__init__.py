from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config = None):
    # create the base app
    app = Flask(__name__)

    # configure app, depending on whether this is a testing context
    if test_config is None:
        app.config.from_pyfile('../settings.cfg')
    else:
        app.config.from_mapping(test_config)

    # initialize and configure database connection
    db = SQLAlchemy(app=app, engine_options={'pool_pre_ping': True,
                                            'isolation_level': 'READ UNCOMMITTED', 'query_cache_size': 0})
    db.init_app(app)

    # incorporate all blueprints
    from . import thing
    app.register_blueprint(thing.blueprint)
    thing.db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    return app
