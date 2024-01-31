from models import User, Like, Listing

from app import db

db.drop_all()
db.create_all()


