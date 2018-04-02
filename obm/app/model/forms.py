from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class ModelForm(FlaskForm):
    model_name = StringField(_l('name of model'), validators=[DataRequired()])
    # model_target = StringField(_l('the class you want to model'), validators=[DataRequired()])
    model_targets = FieldList(StringField(validators=[]),
                              label='the class you want to model', min_entries=2)
    add_target = SubmitField(_('Add'))
    remove_target = SubmitField(_('Remove'))
    submit = SubmitField(_l('Submit'))

    def validate(self):
        if not super(ModelForm, self).validate():
            return False
        val_set = set()
        if " " in self.model_name:
            self.model_name.errors.append("model name cannot contain ' '[space]")
            return False
        for target in self.model_targets:
            if target.data == "":
                msg = "target cannot be empty"
                self.model_targets.errors.append(msg)
                return False
            if target.data not in val_set:
                val_set.add(target.data)
            else:
                msg = "target cannot be duplicated"
                self.model_targets.errors.append(msg)
                return False
        return True


photos = UploadSet('photos', IMAGES)


class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, 'Only picture available'),
        FileRequired('Not choose any file')])
    submit = SubmitField('Upload')