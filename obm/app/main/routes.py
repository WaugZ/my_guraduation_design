import os
import subprocess
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
# from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.models import User, Models
# from app.translate import translate
from app.main import bp






@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('index.html', title=_('Home'))
    page = request.args.get('page', 1, type=int)
    models = current_user.owned_models().paginate(page, current_app.config['MODEL_PER_PAGE'], False)
    next_url = url_for('main.index', page=models.next_num) if models.has_next else None
    prev_url = url_for('main.index', page=models.prev_num) if models.has_prev else None
    return render_template('index.html', title=_('Home'), models=models.items, next_url=next_url,
                           prev_url=prev_url)



