from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class ModelForm(FlaskForm):
    model_name = StringField(_l('name of model'), validators=[DataRequired()])
    model_target = StringField(_l('the class you want to model'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))