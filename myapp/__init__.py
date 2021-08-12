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

    db = SQLAlchemy(app=app, engine_options={'connect_args': {'connect_timeout': 120}, 'pool_pre_ping': True,
                                            'isolation_level': 'READ UNCOMMITTED', 'query_cache_size': 0})
    
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Hello, World!"
    
    return app
