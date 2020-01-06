import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# instantiate the db
db = SQLAlchemy()

# flask toolbar for debugging
toolbar = DebugToolbarExtension()

# flask-cors for cross-origin requests
cors = CORS()

# flask-migration for database migrations
migrate = Migrate()

# flask bcrypt for password hashing
bcrypt = Bcrypt()
