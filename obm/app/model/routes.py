# coding=utf-8
from multiprocessing import Process
import psutil
import os.path as osp
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.model.forms import ModelForm, UploadForm, photos
from app.models import User, Models
from app.model import bp
from app.model_building import auto_modeling
import app.recognition
# from app.recognition import recognize


model_path = "/media/store/paper_data_temp/models"
data_path = "/media/store/paper_data_temp/data"



def complete_check(pid):
    try:
        p = psutil.Process(pid=pid)
        return p.status()
    except psutil.NoSuchProcess:
        return "process has done"


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
        p = Process(name="modeling", target=auto_modeling,
                    args=(form.model_name.data + datetime.now().strftime("%Y%m%d%H%M"), targets,))
        p.daemon = True
        p.start()
        model = Models(model_name=form.model_name.data, model_target=targets, author=current_user,
                       model_path=osp.join(model_path, form.model_name.data + datetime.now().strftime("%Y%m%d%H%M")),
                       pid=p.pid)
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('main.index', title="Home"))

    return render_template('model/new_model.html', form=form, title=_('Create_model'))


@bp.route('/detail/<model_id>', methods=['GET', 'POST'])
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
def check(model_id):
    model = Models.query.filter_by(id=model_id).first()

    if model not in current_user.owned_models():
        flash("You cannot access this model!")
        return redirect(url_for('main.index'))

    statue = complete_check(model.pid)
    if statue == "zomibe" or statue == "process has done":
        model.clean_pid()
        db.session.commit()
    elif statue == "sleeping":
        flash("the model is under construct")
        return render_template('model/detail.html', model=model, title=model.model_name)
    # flash(statue)

    return redirect(url_for('model.detail', model_id=model.id))


@bp.route('/recognize/<model_id>', methods=['GET', 'POST'])
def recognize(model_id):
    model = Models.query.filter_by(id=model_id).first()
    img_name = request.args.get('img_name')
    if model not in current_user.owned_models():
        flash("You cannot access this model!")
        return redirect(url_for('main.index'))
    label, confidence = app.recognition.recognize(model.model_path, img_name)
    return redirect(url_for('model.detail', model_id=model.id, img_name=img_name, label=label, confidence=confidence))


