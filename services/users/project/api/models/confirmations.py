# project/api/models/confirmations.py

from time import time
from uuid import uuid4
from project import db

CONFIRMATION_EXPIRATION_DELTA = 1800


class ConfirmationModel(db.Model):

    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, user_id: int, confirmed=False):
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = confirmed

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def json(self):
        return {
            "id": self.id,
            "expire_at": self.expire_at,
            "confirmed": self.confirmed,
            "user_id": self.user_id,
        }
