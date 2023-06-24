import connexion
from connexion.resolver import RelativeResolver
from flask_jwt_extended import JWTManager

from db import db


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    app.add_api("api.yml", resolver=RelativeResolver("controllers"))

    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
    app.app.config["SECRET_KEY"] = "some-secret-string"

    JWTManager(app.app)

    db.init_app(app.app)
    with app.app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
