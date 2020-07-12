from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RandomForm(FlaskForm):
    numberofusers = IntegerField('numberofusers', validators=[DataRequired()])
    submit = SubmitField('Enter')