from flask import Flask
from models import *
from extensions.database import db
from extensions.login_manager import login_manager


def create_app():
    """Inicializa, configura e retorna o Flask WSGI."""

    app = Flask(__name__)
    app.secret_key = "Use a secret key here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///system.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager.init_app(app)
    db.init_app(app)

    from routes.auth import auth
    app.register_blueprint(auth)

    from routes.system import system
    app.register_blueprint(system)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)