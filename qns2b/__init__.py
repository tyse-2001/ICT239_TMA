from flask import Flask
from flask_session import Session
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = "-YmC0VXwfdWu86mra5TlgIrRDwVs6r8vpPy9bJUxao0"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
    Session(app)

    app.config["MONGODB_SETTINGS"] = {
        "db": "ict239_q2",
        "host": "localhost"
    }
    db = MongoEngine(app)
    app.session_interface = MongoEngineSessionInterface(db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login or register first."

    return app, db, login_manager


app, db, login_manager = create_app()