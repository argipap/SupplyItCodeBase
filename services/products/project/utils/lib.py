# project/utils/lib.py

from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# SQLAlchemy db
db = SQLAlchemy()

# flask toolbar for debugging
toolbar = DebugToolbarExtension()

# flask-cors for cross-origin requests
cors = CORS()

# flask-migration for database migrations
migrate = Migrate()
