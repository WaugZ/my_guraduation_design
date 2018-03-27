# coding=utf-8
import os
import sys
import subprocess
import codecs
from multiprocessing import Process
import psutil
import shutil
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.model.forms import ModelForm, UploadForm, photos
from app.models import User, Models
from app.model import bp


crawl_path = "/media/store/paper_data_temp/crawl"
data_path = "/media/store/paper_data_temp/data"
model_path = "/media/store/paper_data_temp/models"


def crawl_by_name(model_name, model_target):
    crawl_file = os.path.join(crawl_path, model_name + ".txt")
    with codecs.open(crawl_file, 'w', 'utf-8') as file:
        file.write(model_name + "|" + model_target)
        pass
    pwd = os.getcwd()
    os.chdir("/home/train/myTrain/scripts/idt-pitaya-serv-opencv/target")
    input_dir = crawl_file
    output_dir = os.path.join(data_path, model_target)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.call(("sh", "./run.sh", "ImageCrawlerCli", "-input", input_dir, "-output", output_dir))

    os.chdir(pwd)
    sys.exit(0)


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
    if form.validate_on_submit():
        flash("A new model is under construct!")
        p = Process(name="crawl", target=crawl_by_name, args=(form.model_name.data, form.model_target.data))
        p.daemon = True
        p.start()
        model = Models(model_name=form.model_name.data, model_target=form.model_target.data,
                       author=current_user, data_path=data_path, model_path=model_path, pid=p.pid)
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
    if img_name:
        url = photos.url(img_name)
        return render_template('model/detail.html', model=model, title=model.model_name, img_url=url)
    if form.validate_on_submit():
        flash("Checking")
        filename = photos.save(form.photo.data)
        return redirect(url_for('model.detail', model_id=model.id, img_name=filename))
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
