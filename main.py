from flask import Flask
from db import db, mail


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "uma-chave-secreta"

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'brainblazeshop@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vkxs wnor xpaq mdge'

    db.init_app(app)
    mail.init_app(app)

    from views import register_routes
    register_routes(app)

    return app


app = create_app()

from models import User

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)