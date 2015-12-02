# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask_security.utils import login_user, logout_user
from flask_security.decorators import login_required
from flask_security import current_user

from recruit_app.extensions import security, user_datastore
from recruit_app.user.models import User
from recruit_app.public.forms import LoginForm
from recruit_app.utils import flash_errors
from recruit_app.database import db

from recruit_app.blacklist.models import BlacklistCharacter

from recruit_app.user.tasks import run_alliance_corp_update

blueprint = Blueprint('public', __name__, static_folder="../static")

# @login_manager.user_loader
# def load_user(id):
#     return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    return render_template("public/home.html", login_user_form=form)

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    login_user_form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if login_user_form.validate_on_submit():
            login_user(login_user_form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(login_user_form)
    return render_template("public/login.html", login_user_form=login_user_form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", login_user_form=form)
