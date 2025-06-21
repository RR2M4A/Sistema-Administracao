from datetime import timedelta
from flask import Flask, session
from models import *
from extensions import db
from extensions import login_manager


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

    from routes import auth
    app.register_blueprint(auth)

    from routes import system
    app.register_blueprint(system)

    from routes import admin
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=5000, debug=True)
