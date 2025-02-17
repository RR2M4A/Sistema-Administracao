from flask import Flask

def create_app():

    app = Flask(__name__)

    from .auth import auth
    app.register_blueprint(auth)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()