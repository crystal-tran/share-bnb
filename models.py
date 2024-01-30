"""Data models for Share BnB"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of Share BnB"""

    __tablename__ = 'users'

    username = db.Column(
        db.String(30),
        nullable=False,
        primary_key=True,
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default=""
    )


class Listing(db.Model):
    """Listing made by a user"""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    address = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    host_username = db.Column(
        db.String(30),
        db.ForeignKey('users.username'),
        nullable=False
    )

class Photo(db.Model):
    """Photos for listings"""

    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id'),
        nullable=False
    )

    # url that points to photo stored in S3
    photo_url = db.Column(
        db.Text,
        nullable=False
    )