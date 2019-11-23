# services/users/project/__init__.py


import os

from flask import Flask

from project.utils.lib import ma, cors, db, migrate, toolbar


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
    migrate.init_app(app, db)

    # register blueprints
    from project.api.views.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
