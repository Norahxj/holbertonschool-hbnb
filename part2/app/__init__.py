from flask import Flask
from flask_restx import Api
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app, version="1.0", title="HBnB API", prefix="/api/v1")

    # load only the users namespace for now
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns)

    return app
