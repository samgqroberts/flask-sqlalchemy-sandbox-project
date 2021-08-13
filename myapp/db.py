from sqlalchemy import create_engine
from myapp import thing

# common values for development server and testing (but not production)
DEV_DB_USER="root"
DEV_DB_PASSWORD="12345"
DEV_DB_HOST="127.0.0.1"
DEV_DB_PORT="3308"
DEV_DB_CHARSET="utf8mb4"

def direct_connect(user=DEV_DB_USER, password=DEV_DB_PASSWORD, host=DEV_DB_HOST, port=DEV_DB_PORT):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
    conn = engine.connect()
    return conn

def create_database(db_name, user=DEV_DB_USER, password=DEV_DB_PASSWORD, host=DEV_DB_HOST,
                    port=DEV_DB_PORT, charset=DEV_DB_CHARSET):
    conn = direct_connect(user=user, password=password, host=host, port=port)
    conn.execute(f"CREATE DATABASE {db_name} CHARACTER SET {charset}")
    conn.close()

def create_all_tables(app):
    # create db tables for all models declared in blueprints
    with app.app_context():
        thing.db.create_all()

def drop_database(db_name, user=DEV_DB_USER, password=DEV_DB_PASSWORD, host=DEV_DB_HOST,
                  port=DEV_DB_PORT):
    conn = direct_connect(user=user, password=password, host=host, port=port)
    conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
    conn.close()
