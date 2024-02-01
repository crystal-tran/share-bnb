from models import User, Like, Listing, Photo, Booking

from app import db

db.drop_all()
db.create_all()

########################################
#add user


u1 = User.register(
    username="test",
    first_name="Testy",
    last_name="MacTest",
    description="I am the ultimate representative user.",
    email="test@test.com",
    password="secret",
)

u2 = User.register(
    username="test2",
    first_name="Testy2",
    last_name="MacTest2",
    description="I am the ultimate representative user2.",
    email="test2@test2.com",
    password="secret",
)

db.session.add_all([u1, u2])
db.session.commit()

#######################################################
#add property


l1 = Listing(
    title="Suburban backyard",
    description="Great for family gatherings.",
    address="123 Goldspot Dr",
    city="Dallas",
    state="TX",
    zipcode="22222",
    price=100,
    host_id=1

)

l2 = Listing(
    title="Relaxing Retreat at the Pool",
    description="Free Wifi",
    address="457 Ferris Wheel Ct",
    city="San Francisco",
    state="CA",
    zipcode="11111",
    price=400,
    host_id=2
)

db.session.add_all([l1, l2])
db.session.commit()

##################################
#photos

p1 = Photo(
    listing_id=1,
    photo_url="https://platthillnursery.com/wp-content/uploads/2022/03/brand-new-gardens-in-backyard.png"
)

p2 = Photo(
    listing_id=2,
    photo_url="https://png.pngtree.com/background/20230611/original/pngtree-backyard-with-an-inground-pool-and-landscaping-picture-image_3156998.jpg"
)

db.session.add_all([p1, p2])
db.session.commit()


##################################
#bookigns

b1 = Booking(
    listing_id=1,
    renter_id=2
)

b2 = Booking(
    listing_id=2,
    renter_id=1
)

db.session.add_all([b1, b2])
db.session.commit()