from sqlalchemy import UniqueConstraint

from db import db


class User(db.Model):
    """Model User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    files = db.relationship("File", backref="user", lazy=True)


class File(db.Model):
    """Model File"""
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint("filename", "user_id"),)
