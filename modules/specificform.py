from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class SpecificForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    submit = SubmitField('Enter')