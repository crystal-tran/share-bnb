"""Flask App for Share BnB"""

import os

from flask import Flask, render_template, request, flash, g
from flask import redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import CSRFProtectForm, RegisterForm, LoginForm, AddListingForm
from werkzeug.utils import secure_filename
from models import db, connect_db, User, Like, Listing, Photo, Booking
from s3_config import upload_file, create_presigned_url, allowed_file
import uuid


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebnb')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

# toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = "curr_user"

connect_db(app)


####################### TESTING ###########################
# @app.route('/', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         # check if the post request has the file part

#         file = request.files['file']

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             new_filename = uuid.uuid4().hex + '.' + filename.rsplit('.', 1)[1].lower()
#             upload_file(file, new_filename)
#             url = create_presigned_url(new_filename)
#             print("**new_filename", new_filename)
#             print("***url", url )
#     return render_template("upload.html")

# Authorization
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    # session.clear()

    if CURR_USER_KEY in session:
        # print("#####session", session[CURR_USER_KEY])
        g.user = User.query.get(session[CURR_USER_KEY])
        # print("####g.user", g.user)

    else:
        g.user = None


@app.before_request
def add_csrf_to_g():
    """Add a cssrf form to Flask global."""
    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """ Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.

    Create a new user and add to DB. Redirect to home page.

    If form is not valid, present the form.

    If there already is a user with that username: flash message and present
    the form.
    """
    do_logout()
    print("register route:")

    form = RegisterForm()

    if form.validate_on_submit():
        print("register: validating form")
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username/email already taken", 'danger')
            return render_template('users/register.html', form=form)

        do_login(user)
        return redirect("/")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login. Redirect to home upon success"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}", "success")
            return redirect("/")

        flash("Invalid username/password", "danger")

    return render_template('users/login.html', form=form)


@app.post('/logout')
def logout():
    """Hanlde logout of user. Redirect to hompage"""

    form = g.csrf_form
    print("1) g user:", g.user)

    if not form.validate_on_submit() or not g.user:
        flash("Unauthorized", "danger")
        print("2) g user:", g.user)
        return redirect("/")

    do_logout()
    print("3) g user:", g.user)

    flash("You have successfully logged out", "success")
    return redirect("/")


# Homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")

# Listings


@app.get("/listings")
def list_listings():
    """Show page with listings."""

    search_title = request.args.get('search-title')
    search_city = request.args.get('search-city')
    print("search title:", search_title)
    print("search_city:", search_city)

    if not search_title and not search_city:
        listings = Listing.query.all()
        print("query listing:", listings)

    else:
        listings = Listing.query.filter(
            Listing.title.ilike(f"%{search_title}%"),
            Listing.city.ilike(f"%{search_city}%"),
            ).all()
        print("query filter listing:", listings)

    return render_template("listings/listings.html", listings=listings)

@app.get("/listings/<int:listing_id>")
def listing_detail(listing_id):
    """Show an individual listing"""

    listing = Listing.query.get_or_404(listing_id)

    return render_template("listings/detail.html", listing=listing)

###################################### User

# @app.route("/users/<int:user_id>/")
# def add_listings():
#     """Show form to add a listing and handles form submission."""

#     if not g.user:
#         flash("Unauthorized", "danger")
#         return redirect("/")

#     form = request.forms

@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Show user profile with hosted listings."""

    if not g.user:
        flash("Unauthorized", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)

@app.route("/users/<int:user_id>/add-listing", methods=["GET", "POST"])
def add_listing(user_id):
    """Show form for adding a listing.

    Add lisiting to database.

    """
    if not g.user:
        flash("Unauthorized", "danger")
        return redirect("/")

    form = AddListingForm()

    if form.validate_on_submit():
        new_listing = Listing.add_listing(
            title = form.title.data,
            description = form.description.data,
            address = form.address.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            price=form.price.data,
            host_id= g.user.id
        )
        db.session.commit()

        # photo = request.files["file"]
        photos = request.files.to_dict("file")
        # breakpoint()
        print("photos from request.files.getlist", photos)
        for photo in photos:
            print("photo in photos", photos[photo])
        # print("***form photo:", photo)
        if photo and allowed_file(photo.filename):
            # sanitizes photo inputs
            photo_name = secure_filename(photo.filename)
            # gives a unique photo name
            new_photo_name = uuid.uuid4().hex + '.' + photo_name.rsplit('.', 1)[1].lower()

            #upload file to AWS S3 bucket
            upload_file(photo, new_photo_name)
            #create photo url to store in db
            photo_url = create_presigned_url(new_photo_name)

            listing_photo = Photo(
                listing_id= new_listing.id,
                photo_url = photo_url
            )

            db.session.add(listing_photo)
            print("***photo_name:", new_photo_name)
            print("photo_url:", photo_url)

        db.session.commit()

        flash(f"{new_listing.title} added", "success")
        return redirect(f"/users/{user_id}")

    return render_template("listings/add-listing.html", form=form)



#######################################
# API for booking

@app.get("/api/bookings")
def bookings_listing():
    """Did user book this listing?"""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    listing_id = int(request.args['listing_id'])
    listing = Listing.query.get_or_404(listing_id)

    booking = Booking.query.filter_by(renter_id=g.user.id, listing_id=listing.id).first()
    booked = booking is not None

    return jsonify(booked = booked)


@app.post("/api/book")
def book_listing():
    """Book a listing"""

    print("book listing route")
    if not g.user:
        return jsonify({"error": "Not logged in"})

    data = request.json
    print("data is:", data)

    listing_id = int(data['listing_id'])
    print('listing_id:', listing_id)
    listing = Listing.query.get_or_404(listing_id)
    print("book listing:", listing)

    g.user.booked_listings.append(listing)
    db.session.commit()

    res = {"booked": listing.id}
    return jsonify(res)


@app.post("/api/cancel")
def cancel_listing():
    """Cancel a booked listing"""

    print("cancel listing route")

    if not g.user:
        return jsonify({"error": "Not logged in"})

    data = request.json
    listing_id = int(data['listing_id'])
    print('cancel listing_id:', listing_id)
    listing = Listing.query.get_or_404(listing_id)
    print("cancel listing:", listing)


    Booking.query.filter_by(listing_id=listing_id, renter_id=g.user.id).delete()
    db.session.commit()

    res = {"canceled": listing.id}
    return jsonify(res)

