"""Data models for Share BnB"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User of Share BnB"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    password = db.Column(
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

    @classmethod
    def register(cls, username, first_name, last_name, email, description, password):
        """Register user and hasehs password. Adds user to session.

        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            description=description,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find a user with provided username and password

        Returns user if user is found, otherwise returns False
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            auth_user= bcrypt.check_password_hash(user.password, password)
            if auth_user:
                return user

        return False


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

    city = db.Column(
        db.String(50),
        nullable=False
    )

    state = db.Column(
        db.String(2),
        nullable=False
    )

    zipcode = db.Column(
        db.String(10),
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    host_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id'),
        nullable=False
    )

    # renter_id = db.Column(
    #     db.Integer(),
    #     db.ForeignKey('users.id'),
    #     nullable=False,
    #     default=0
    # )

    # relationship between User and Listing
    host_user = db.relationship('User', foreign_keys=[host_id], backref="host_listings")
    # renter_user = db.relationship('User', foreign_keys=[renter_id], backref="renter_listings")

    @classmethod
    def add_listing(cls, title, description, address, city, state, zipcode, price, host_id):
        new_listing = Listing (
            title = title,
            description = description,
            address = address,
            city = city,
            state = state,
            zipcode = zipcode,
            price=price,
            host_id= host_id
        )

        db.session.add(new_listing)

        return new_listing

class Renter(db.Model):
    """Renter listing and id"""
    __tablename__ = 'renters'

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id'),
        primary_key=True
    )

    renter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

class Photo(db.Model):
    """Photos for a listing"""

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

    # relationship between Photo and Listing
    listings = db.relationship('Listing', backref='photos')


class Like(db.Model):
    """A user can like a listing."""

    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id'),
        primary_key=True,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id'),
        primary_key=True
    )

    # TODO: Class Message


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
