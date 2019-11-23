# services/users/project/__init__.py


import os

from flask import Flask

# first we need to intialize flask sqlalchemy and then marshmallow!!
from project.utils.sqlalc import db
from project.utils.ma import ma
from project.utils.toolbar import toolbar
from project.utils.flaskcors import cors


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    ma.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)

    # register blueprints
    from project.api.views.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
