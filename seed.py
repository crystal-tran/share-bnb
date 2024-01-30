from models import User, Likes, db, Listing

from app import app

db.drop_all()
db.create_all()


