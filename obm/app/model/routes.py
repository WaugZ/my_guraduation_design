# coding=utf-8
import requests
import os.path as osp
from datetime import datetime
import json
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.model.forms import ModelForm, UploadForm, photos
from app.models import User, Models
from app.model import bp
from config import ServerConfig


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/new_model', methods=['GET', 'POST'])
# @login_required
def new_model():
    if not current_user.is_authenticated:
        flash("You have to login first")
        return render_template('index.html', title=_('Home'))

    form = ModelForm()
    if form.add_target.data:
        form.model_targets.append_entry('')
    elif form.remove_target.data:
        form.model_targets.pop_entry()
    elif request.form and form.validate_on_submit():
        flash("A new model is under construct!")
        targets = ""
        for target in form.model_targets.data:
            targets += target + "#"
        targets = targets[:-1]  # delete the last '#'
        now = datetime.now().strftime("%Y%m%d%H%M")
        data = {'name': form.model_name.data + now, 'targets': targets}
        r = requests.post("http://localhost:9999", data=data)

        flash(r.text)

        model = Models(model_name=form.model_name.data, model_target=targets, author=current_user,
                       model_path=osp.join(ServerConfig.MODEL_PATH, form.model_name.data + now), timestamp=datetime.now())
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('main.index', title="Home"))

    return render_template('model/new_model.html', form=form, title=_('Create_model'))


@bp.route('/detail/<model_id>', methods=['GET', 'POST'])
@login_required
def detail(model_id):
    model = Models.query.filter_by(id=model_id).first()
    if model not in current_user.owned_models():
        flash("You cannot access this model!")
        return redirect(url_for('main.index'))
    form = UploadForm()
    img_name = request.args.get('img_name')
    label = request.args.get('label')
    confidence = request.args.get('confidence')
    if img_name and label and confidence:
        url = photos.url(img_name)
        return render_template('model/detail.html', model=model, title=model.model_name,
                               img_url=url, label=label, confidence=confidence)
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        return redirect(url_for('model.recognize', model_id=model.id, img_name=filename))
        # return redirect(url_for('model.detail', model_id=model.id, img_name=filename))
    return render_template('model/detail.html', model=model, title=model.model_name, form=form)


@bp.route('/check/<model_id>', methods=['GET'])
@login_required
def check(model_id):
    model = Models.query.filter_by(id=model_id).first()

    if model not in current_user.owned_models():
        flash("You cannot access this model!")
        return redirect(url_for('main.index'))

    if model.statue:
        return redirect(url_for('model.detail', model_id=model.id))

    data = {"model_path": model.model_path}
    r = requests.post("http://localhost:9999/check", data=data)
    if r.text == "complete":
        model.complete()
        db.session.commit()
        return redirect(url_for('model.detail', model_id=model.id))
    else:
        ts = datetime.now() - model.timestamp
        ts = ts.seconds
        if ts > 30 * 60:  # longer than 30 min
            flash("the model is under construct(if it has been a long time, you may re-build it)")
        else:
            flash("the model is under construct")
        return render_template('model/detail.html', model=model, title=model.model_name)


@bp.route('/recognize/<model_id>', methods=['GET', 'POST'])
@login_required
def recognize(model_id):
    model = Models.query.filter_by(id=model_id).first()
    img_name = request.args.get('img_name')
    if model not in current_user.owned_models():
        flash("You cannot access this model!")
        return redirect(url_for('main.index'))

    data = {"model_path": model.model_path, "img_name": img_name}
    r = requests.post("http://localhost:9998", data=data)
    msg = json.loads(r.text)
    label = msg['label']
    confidence = msg['confidence']
    return redirect(url_for('model.detail', model_id=model.id, img_name=img_name, label=label, confidence=confidence))


