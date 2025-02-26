from flask import Flask
from models import *
from database import db


def create_app():

    app = Flask(__name__)
    app.secret_key = "Use a secret key here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///system.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from auth import auth
    app.register_blueprint(auth)

    from main import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)