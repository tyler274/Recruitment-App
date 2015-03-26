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
from recruit_app.user.forms import RegisterForm
from recruit_app.utils import flash_errors
from recruit_app.database import db

from recruit_app.user.managers import AuthInfoManager

blueprint = Blueprint('public', __name__, static_folder="../static")

# @login_manager.user_loader
# def load_user(id):
#     return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    AuthInfoManager.get_or_create(current_user.get_id())
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", login_user_form=form)

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    login_user_form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/login.html", login_user_form=login_user_form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))

# @blueprint.route("/register/", methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form, csrf_enabled=False)
#     if form.validate_on_submit():
#         new_user = User.create(username=form.username.data,
#                         email=form.email.data,
#                         password=form.password.data,
#                         active=True)
#         # user_datastore.create_user(email=form.email.data, username=form.username.data, password=form.password.data, active=True)
#         AuthInfoManager.get_or_create(current_user.get_id())

#         flash("Thank you for registering. You can now log in.", 'success')
#         return redirect(url_for('public.home'))
#     else:
#         flash_errors(form)
#     return render_template('public/register.html', form=form)

@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", login_user_form=form)
