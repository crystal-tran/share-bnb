"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileRequired, MultipleFileField, FileAllowed


class LoginForm(FlaskForm):
    """FOrm for logging in a user"""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
        default='guest',
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
        default='password',
    )


class RegisterForm(FlaskForm):
    """Form for adding users on signup."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    first_name = StringField(
        'First Name',
        validators=[InputRequired(), Length(max=50)],
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired(), Length(max=50)],
    )

    description = TextAreaField(
        'Description',
    )

    email = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )


class AddListingForm(FlaskForm):
    """Form for adding a property listing"""

    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=50)],
        default="Outdoor Lakehouse",
    )

    description = TextAreaField(
        'Description',
        default="Fire pits, boats, kayaks, paddleboards, fishing, and more!",
    )

    address = StringField(
        'Address',
        validators=[InputRequired()],
        default="444 Lake Pike",
    )

    city = StringField(
        'City',
        validators=[InputRequired(), Length(max=50)],
        default="Salt Lake City",
    )

    state = StringField(
        'State',
        validators=[InputRequired(), Length(max=2)],
        default="UT",
    )

    zipcode = StringField(
        'Zipcode',
        validators=[InputRequired(), Length(max=10)],
        default="41489",
    )

    price = DecimalField(
        'Rental Price',
        validators=[InputRequired()],
        default=200,
    )

    photo = MultipleFileField(
        'Photo(s)',
        validators=[FileRequired(),
                    FileAllowed(['png', 'jpg', 'jpeg'])]
    )


# class TestingUploadForm(FlaskForm):
#     photo = FileField(
#         'Photo',
#         validators=[InputRequired()]
#     )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""
