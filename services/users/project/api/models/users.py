# project/api/models/users.py
import datetime
import enum
import jwt
from sqlalchemy.sql import func
from flask import current_app
from project import db, bcrypt


class UserType(enum.Enum):
    retail = 1
    wholesale = 2


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    user_type = db.Column(db.Enum(UserType), default=UserType.retail, nullable=False)
    retailer = db.relationship("RetailerModel", backref="user", uselist=False)
    supplier = db.relationship("SupplierModel", backref="user", uselist=False)

    def __init__(
        self, username, email, password, admin=False, user_type=UserType.retail
    ):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
        self.user_type = user_type
        self.admin = admin

    @classmethod
    def encode_auth_token(cls, user_id):
        """Generates the auth token"""
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=current_app.config.get("TOKEN_EXPIRATION_DAYS"),
                    seconds=current_app.config.get("TOKEN_EXPIRATION_SECONDS"),
                ),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(
                payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e

    @classmethod
    def decode_auth_token(cls, token):
        """Decodes auth token given"""
        try:
            payload = jwt.decode(
                token, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
            "admin": self.admin,
            "user_type": self.user_type.name,
        }
