# project/api/models/users.py

import os
import datetime
import enum
import jwt
from sqlalchemy.sql import func
from flask import current_app, request, url_for
from project import db, bcrypt
from project.api.models.confirmations import ConfirmationModel
from project.utils.mailgun import Mailgun


class UserType(enum.Enum):
    retail = 1
    wholesale = 2


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    user_type = db.Column(db.Enum(UserType), default=UserType.retail, nullable=False)
    retailer = db.relationship(
        "RetailerModel", backref="user", uselist=False, cascade="all, delete-orphan",
    )
    supplier = db.relationship(
        "SupplierModel", backref="user", uselist=False, cascade="all, delete-orphan",
    )
    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(
        self, username, email, password, admin=False, user_type=UserType.retail,
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

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def send_confirmation_mail(self):
        subject = "Registration Confirmation"
        link = (
            f"{os.environ.get('REACT_APP_USERS_SERVICE_URL', 'http://localhost')}"
            f"/users/user/confirmation/{self.most_recent_confirmation.id}"
        )
        # link = request.url_root[:-1] + url_for(
        #     "/users/user/confirmation",
        #     confirmation_id=self.most_recent_confirmation.id
        # )
        text = f"Please click the link to confirm your registration: {link}"
        html = (
            f"<html>Please click the link to confirm your registration:"
            f"<a href={link}>link</a></html>"
        )
        response = Mailgun.send_email(
            ["argipapaefstathiou@gmail.com"], subject, text, html
        )
        return response

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "admin": self.admin,
            "user_type": self.user_type.name,
        }
