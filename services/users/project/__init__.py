# services/users/project/__init__.py


import os
from flask import Flask
from project.utils.lib import cors, db, migrate, toolbar, bcrypt


def register_blueprints(app):
    from project.api.views.users import users_blueprint

    app.register_blueprint(users_blueprint)
    from project.api.views.auth import auth_blueprint

    app.register_blueprint(auth_blueprint)
    from project.api.views.suppliers import suppliers_blueprint

    app.register_blueprint(suppliers_blueprint)
    from project.api.views.retailers import retailers_blueprint

    app.register_blueprint(retailers_blueprint)
    from project.api.views.addresses import addresses_blueprint

    app.register_blueprint(addresses_blueprint)
    from project.api.views.stores import stores_blueprint

    app.register_blueprint(stores_blueprint)
    from project.api.views.companies import companies_blueprint

    app.register_blueprint(companies_blueprint)


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    register_blueprints(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
