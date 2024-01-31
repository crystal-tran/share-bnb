"""Flask App for Share BnB"""

import os

from flask import Flask, render_template, request, flash, g
from flask import redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import TestingUploadForm, CSRFProtectForm, RegisterForm
from werkzeug.utils import secure_filename
from models import db, connect_db, User, Like, Listing, Photo
from s3_config import upload_file, create_presigned_url, allowed_file
import uuid



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebnb')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

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

################################# Authorization
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    # session.clear()

    if CURR_USER_KEY in session:
        print("#####session", session[CURR_USER_KEY])
        g.user = User.query.get(session[CURR_USER_KEY])
        print("####g.user", g.user)


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

################################# Homepage
@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")