import uuid

from sqlalchemy.sql import func

from app.db import db
from app.exceptions.custom_exceptions import DatabaseOperationError


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(64), primary_key=True, nullable=False)
    username = db.Column(db.String(64), nullable=False,
                         index=True, unique=True)
    email = db.Column(db.String(128), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(),
                           onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username}>"

    def __init__(self, username, email, password_hash):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.filter_by(id=id).first()
        except Exception as e:
            raise DatabaseOperationError(
                "Error getting user by ID: " + str(e))

    @classmethod
    def get_by_username(cls, username):
        try:
            return cls.query.filter_by(username=username).first()
        except Exception as e:
            raise DatabaseOperationError(
                "Error getting user by username: " + str(e))

    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).first()
        except Exception as e:
            raise DatabaseOperationError(
                "Error getting user by email: " + str(e))

    @classmethod
    def create(cls, username, email, password_hash):
        user = cls(username, email, password_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseOperationError(
                "Error creating user: " + str(e))
