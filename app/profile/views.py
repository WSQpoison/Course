import os
import random

from . import profile
from flask import Flask, render_template, redirect, url_for, flash, session
from flask import request
from flask_login import UserMixin, login_required
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from .forms import *
from ..models import *
from .. import db
from ..util import *

basedir = 'app'

@profile.route('/profile_user/<id>')
def profile_user(id):
    head = get_user_head(id)
    user = User.query.filter_by(id=id).first()
    return render_template('profiles/profile_user.html', user=user, head=head)

@profile.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        head = form.head.data
        if head != '':
            for f in os.listdir('app/static/heads'):
                if f.startswith(str(current_user.id)):
                    os.remove(os.path.join('app/static/heads', f))
            filename = secure_filename(head.filename)
            head.save(os.path.join(
                basedir, 'static', 'heads',
                str(current_user.id) + str(random.choice(range(100))) + '.jpg'
            ))
        db.session.add(current_user)
        db.session.commit()
        flash('个人简介更新成功')
        return redirect(url_for('.profile_user', id=current_user.id))
    form.email.data = current_user.email
    return render_template('profiles/profile_edit.html', form=form)