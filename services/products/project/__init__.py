# project/__init__.py


import os

from flask import Flask
from project.utils.lib import cors, toolbar, db, migrate


def register_blueprints(app):
    # register blueprints
    from project.api.views.base import base_blueprint
    from project.api.views.products import products_blueprint

    app.register_blueprint(base_blueprint)
    app.register_blueprint(products_blueprint)


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    toolbar.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    register_blueprints(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
