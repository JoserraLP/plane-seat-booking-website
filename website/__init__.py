from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager

from .redis.redisdb import RedisDB
from redlock import Redlock

from config import default
from static import constants

# init SQLAlchemy
db = SQLAlchemy()

# Create Redlock instance
redlock = Redlock([{"host": constants.REDLOCK_HOST, "port": constants.REDLOCK_PORT, "db": constants.REDLOCK_DB, "password": constants.REDIS_PASSWORD},])

# Included all the replicas but they are only read

# Create a Redis instance
redis = RedisDB(host=constants.REDIS_HOST, port=constants.REDIS_PORT, db=constants.REDIS_DB)

# Create a Redis instance
redis_lock = RedisDB(host=constants.REDIS_HOST, port=constants.REDIS_PORT, db=constants.REDLOCK_DB)


def create_app():
    """
    Create a Flask app, configure it. register some project blueprints as 'auth' or 'main',
    initialize related services as MQTT or SQLAlchemy (with data insertion) and the flask login manager.

    Returns:
        app (object): Configured Flask app

    """
    # Create Flask app 
    app = Flask(__name__, instance_relative_config=True)

    # Configure the application with the config file
    app.config.from_object(default)

    # Register project blueprints 

    # -> Auth routes
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # -> Non-auth routes 
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # -> Planes routes
    from planes import planes as planes_blueprint
    app.register_blueprint(planes_blueprint)

    # -> Admin routes
    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # Import models to create the tables
    from models import User, Role

    # Init the Flask-User Manager service 
    user_manager = UserManager(app, db, User)

    # Init the SQLAlchemy - DB service
    db.init_app(app)

    # Create the tables with the application context
    with app.app_context():
        db.create_all()
        # If there are no users and no roles create and insert them on the db
        if not User.query.limit(1).all() and not Role.query.limit(1).all():
            from website.utils.insert_data_to_db import insert_user_data
            insert_user_data(db)

    # Create the LoginManager
    login_manager = LoginManager()

    # Set the login manager main view as the login service
    login_manager.login_view = 'auth.login'

    # Init the LoginManager service
    login_manager.init_app(app)

    # Define the user loader for the LoginManager
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        try:
            return User.query.get(int(user_id))
        except:
            return None

    return app
