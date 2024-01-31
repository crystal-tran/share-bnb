"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, FileField
from wtforms.validators import InputRequired, Email, Length


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
    )

    description = TextAreaField(
        'Description',
    )

    address = StringField(
        'Address',
        validators=[InputRequired()],
    )

    city = StringField(
        'City',
        validators=[InputRequired(), Length(max=50)],
    )

    state = StringField(
        'State',
        validators=[InputRequired(), Length(max=2)],
    )

    zipcode = StringField(
        'Zipcode',
        validators=[InputRequired(), Length(max=10)],
    )

    price = DecimalField(
        'Rental Price',
        validators=[InputRequired()],
    )

    photo = StringField(
        'State',
        validators=[InputRequired()],
    )



class TestingUploadForm(FlaskForm):
    photo = FileField(
        'Photo',
        validators=[InputRequired()]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""
