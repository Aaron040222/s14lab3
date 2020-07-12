from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class DeleteForm(FlaskForm):
    user_id = IntegerField('user_id', validators=[DataRequired()])
    submit = SubmitField('Enter')