from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length, ValidationError
from enums import State, Genres

def multiple_field_validator(options):
    '''Custom validator for multiple selector '''
    def inner_function(form, field):
        for value in field.data:
            if value not in [ option.value for option in options ]:
                raise ValidationError('Valid enums are %s' % ([option.value for option in options]))
    return inner_function




class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf([ choice.value for choice in State ])],
        choices=State.options()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), multiple_field_validator],
        choices=Genres.options()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = TextAreaField(
        'Text', render_kw={"rows": 3, "cols": 11}
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf ([ choice.value for choice in State ])],
        choices=State.options()
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), multiple_field_validator(Genres)],
        choices=Genres.options()
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = TextAreaField(
        'Text', render_kw={"rows": 3, "cols": 11}
    )
    website = StringField(
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

