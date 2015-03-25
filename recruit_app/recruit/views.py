from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted

from recruit_app.user.managers import EveManager, AuthInfoManager
from recruit_app.user.eve_api_manager import EveApiManager
from recruit_app.user.forms import UpdateKeyForm

from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair
from recruit_app.recruit.models import HrApplication
from recruit_app.recruit.managers import HrManager
from recruit_app.recruit.forms import HrApplicationForm

import datetime as dt

blueprint = Blueprint("recruit", __name__, url_prefix='/recruits',
                        static_folder="../static")

@blueprint.route("/applications/", methods=['GET', 'POST'])
@login_required
def applications():
    applications = []
    authinfo = []
    if HrApplication.query.filter_by(user_id=current_user.get_id()).first():
        # characters = EveManager.get_characters_by_owner_id(current_user.get_id())
        applications = HrApplication.query.filter_by(user_id=current_user.get_id()).all()

    if AuthInfoManager.get_or_create(current_user.get_id()):
        authinfo = AuthInfoManager.get_or_create(current_user.get_id())

    return render_template('recruit/applications.html', authinfo=authinfo, applications=applications)


@blueprint.route("/applications/<application_id>/", methods=['GET', 'POST'])
@login_required
def application_view(application_id):
    user_id = current_user.get_id()
    comments = []

    if AuthInfoManager.get_or_create(current_user.get_id()):
        auth_info = AuthInfoManager.get_or_create(current_user.get_id())

    if HrManager.check_if_application_owned_by_user(application_id, user_id):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            application = HrApplication.query.filter_by(id=int(application_id)).first()
            return render_template('recruit/application.html',
                               auth_info=auth_info,
                               current_user=current_user,
                               application=application,
                               comments=comments)

    if request.method == 'POST':
        pass

    return redirect(url_for('recruit.applications'))

@blueprint.route("/applications/<application_id>/<action>", methods=['GET', 'POST'])
@login_required
def application_interact(application_id, action):
    user_id = current_user.get_id()
    comments = []

    if AuthInfoManager.get_or_create(current_user.get_id()):
        auth_info = AuthInfoManager.get_or_create(current_user.get_id())

    if HrApplication.query.filter_by(id=int(application_id)).first():
        application = HrApplication.query.filter_by(id=int(application_id)).first()

        # alter_application takes one of 4 actions
        if current_user.has_role("admin") or current_user.has_role("recruiter"):
            application_status = HrManager.alter_application(application_id, action, user_id)

            flash("%s's application %s" % (application.main_character, application_status), category='message')

        elif application.user_id == user_id:
            if action == "delete" and application.approve_deny == "Pending":
                application_status = HrManager.alter_application(application_id, action, user_id)


        if application_status and application_status != "deleted":
            return redirect(url_for('recruit.application_view', application_id=application.id))

    return redirect(url_for('recruit.applications'))







