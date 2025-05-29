from flask import Flask, session, request, redirect, url_for
from models import *
from extensions.database import db
from extensions.login_manager import login_manager
from datetime import timedelta
from flask_login import current_user


def create_app():
    """Inicializa, configura e retorna o Flask WSGI."""

    app = Flask(__name__)

    app.secret_key = "Use a secret key here"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///system.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)


    login_manager.init_app(app)
    db.init_app(app)

    from routes.auth import auth
    app.register_blueprint(auth)

    from routes.system import system
    app.register_blueprint(system)

    from routes.admin import admin
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)