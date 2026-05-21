#validators
import re
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, FloatField,
                     SelectField, BooleanField, IntegerField)
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                NumberRange, Optional, ValidationError)

# Form classes for user registration, login, listings, messages, reviews,
# reports, profiles, and collections. Validators help prevent missing,
# invalid, or overly long user input.

ALLOWED_CONDITIONS = ['mint', 'near_mint', 'light_played', 'played', 'damaged']
ALLOWED_FINISHES = ['non_holo', 'holo', 'reverse_holo', 'foil', 'sir', 'alt_art']


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])


class LoginForm(FlaskForm):
    email = StringField('Email / Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ListingForm(FlaskForm):
    card_id = StringField('Card', validators=[DataRequired()])
    condition = SelectField('Condition', choices=[
        ('near_mint', 'Near Mint'), ('mint', 'Mint'),
        ('light_played', 'Light Played'), ('played', 'Played'), ('damaged', 'Damaged'),
    ], validators=[DataRequired()])
    finish = SelectField('Finish', choices=[
        ('non_holo', 'Non-Holo'), ('holo', 'Holo'), ('reverse_holo', 'Reverse Holo'),
        ('foil', 'Foil'), ('sir', 'SIR'), ('alt_art', 'Alt Art'),
    ], validators=[DataRequired()])
    price = FloatField('Price (NZD)', validators=[DataRequired(), NumberRange(min=0.01, max=99999)])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=100)], default=1)
    notes = TextAreaField('Notes / Card Details', validators=[Optional(), Length(max=1000)])
    delivery_type = SelectField('Delivery', choices=[
        ('both', 'Pick-up or Shipped'), ('pickup', 'Pick-up Only'), ('shipped', 'Shipped Only'),
    ])
    shipping_cost = FloatField('Shipping Cost (NZD)', validators=[Optional(), NumberRange(min=0)], default=10.0)


class MessageForm(FlaskForm):
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ('5', '5 — Excellent'), ('4', '4 — Good'), ('3', '3 — Okay'),
        ('2', '2 — Poor'), ('1', '1 — Terrible'),
    ], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=1000)])


class ReportForm(FlaskForm):
    reason = SelectField('Reason', choices=[
        ('counterfeit', 'Counterfeit card'), ('fraud', 'Fraud / scam'),
        ('wrong_condition', 'Condition misrepresented'), ('spam', 'Spam'),
        ('other', 'Other'),
    ], validators=[DataRequired()])
    details = TextAreaField('Details', validators=[Optional(), Length(max=1000)])


class ProfileForm(FlaskForm):
    store_name = StringField('Store Name', validators=[Optional(), Length(max=100)])
    store_description = TextAreaField('Store Description', validators=[Optional(), Length(max=500)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])


class CollectionForm(FlaskForm):
    name = StringField('Collection Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    total_cards_needed = IntegerField('Set Size (total cards)', validators=[Optional(), NumberRange(min=0)], default=0)
