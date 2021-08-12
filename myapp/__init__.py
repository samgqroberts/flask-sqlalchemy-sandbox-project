from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('../settings.cfg')
    db = SQLAlchemy(app=app, engine_options={'connect_args': {'connect_timeout': 120}, 'pool_pre_ping': True,
                                            'isolation_level': 'READ UNCOMMITTED', 'query_cache_size': 0})
    
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Hello, World!"
    
    return app
