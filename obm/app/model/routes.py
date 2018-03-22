from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
# from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.model.forms import ModelForm
from app.models import User, Models
# from app.translate import translate
from app.model import bp


data_path = "/"
model_path = "/"


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/new_model', methods=['GET', 'POST'])
# @login_required
def new_model():
    if not current_user.is_authenticated:
        flash("You have to login first")
        return render_template('index.html', title=_('Home'))

    form = ModelForm()
    if form.validate_on_submit():
        model = Models(model_name=form.model_name.data, model_target=form.model_target.data,
                       author=current_user, data_path=data_path, model_path=model_path)
        db.session.add(model)
        db.session.commit()
        flash("A new model is under construct!")
        # return redirect(url_for('model/<form.model_name.data>'))  # in the future version, it will jump to model page
        return redirect(url_for('main.index'))

    return render_template('model/new_model.html', form=form, title=_('New_model'))


