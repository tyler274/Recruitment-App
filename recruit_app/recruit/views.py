from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted

from recruit_app.user.managers import EveManager, AuthInfoManager
from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, User
from recruit_app.recruit.models import HrApplication, HrApplicationComment
from recruit_app.recruit.managers import HrManager
from recruit_app.recruit.forms import HrApplicationForm, HrApplicationCommentForm, SearchForm

from flask_sqlalchemy import Pagination

import datetime as dt

blueprint = Blueprint("recruit", __name__, url_prefix='/recruits',
                        static_folder="../static")

@blueprint.route("/applications/", methods=['GET', 'POST'])
@login_required
def applications():
    applications = []
    authinfo = []
    search_results = []

    recruiter_queue = []

    search_form = SearchForm()

    if HrApplication.query.filter_by(user_id=current_user.get_id()).first():
        # characters = EveManager.get_characters_by_owner_id(current_user.get_id())
        applications = HrApplication.query.filter_by(user_id=current_user.get_id()).all()

    if AuthInfoManager.get_or_create(current_user.get_id()):
        authinfo = AuthInfoManager.get_or_create(current_user.get_id())

    if current_user.has_role("recruiter") or current_user.has_role("admin"):
        # recruiter_queue = HrApplication.query.filter(
        #     HrApplication.hidden == False,
        #     (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided") ).all()
        query = HrApplication.query.filter(HrApplication.hidden == False,
                                           (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided"))
        recruiter_queue = query.paginate(1, 3, False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            search_results = HrApplication.query.whoosh_search(search_form.search.data).all()
            recruiter_queue = search_results

    return render_template('recruit/applications.html',
                           applications=applications,
                           recruiter_queue=recruiter_queue,
                           search_form=search_form,
                           search_results=search_results)


@blueprint.route("/application_queue/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/<option>/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def application_queue(option=None, page=1):
    applications = []
    authinfo = []
    search_results = []

    recruiter_queue = []

    search_form = SearchForm()

    if AuthInfoManager.get_or_create(current_user.get_id()):
        authinfo = AuthInfoManager.get_or_create(current_user.get_id())

    # recruiter_queue = HrApplication.query.filter(
    #     HrApplication.hidden == False,
    #     (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided") ).all()
    query = HrApplication.query.filter(HrApplication.hidden == False,
                                       (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided")).order_by(HrApplication.id)
    recruiter_queue = query.paginate(page, 5, False)


    if request.method == 'POST':
        if search_form.validate_on_submit():
            search_results = HrApplication.query.whoosh_search(search_form.search.data + "*")
            recruiter_queue = search_results.paginate(page, 5, False)

    if option == "all":
        recruiter_queue = query.paginate(page, error_out=False)

    elif option == "history":
        recruiter_queue = HrApplication.query.order_by(HrApplication.id)

    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form,
                           search_results=search_results)


@blueprint.route("/applications/create/", methods=['GET', 'POST'])
@login_required
def application_create():
    user_id = current_user.get_id()
    applications = []
    authinfo = []
    character_choices = []

    if AuthInfoManager.get_or_create(current_user.get_id()):
        authinfo = AuthInfoManager.get_or_create(current_user.get_id())

    form = HrApplicationForm()

    for character in EveCharacter.query.filter_by(user_id=user_id).all():
        character_choices = character_choices + [(character.character_id, character.character_name)]

    form.characters.choices = character_choices

    if request.method == 'POST':
        if form.validate_on_submit():
            HrManager.create_application(how_long=form.how_long.data,
                                         have_done=form.have_done.data,
                                         scale=form.data['scale'],
                                         reason_for_joining=form.data['reason_for_joining'],
                                         favorite_ship=form.data['favorite_ship'],
                                         favorite_role=form.data['favorite_role'],
                                         most_fun=form.data['most_fun'],
                                         main_character_name=current_user.auth_info[0].main_character.character_name,
                                         user_id=user_id,
                                         characters=form.characters.data)

            flash("Application Created", category='message')
            return redirect(url_for('recruit.applications'))

    return render_template('recruit/application_create.html',
                           authinfo=authinfo,
                           form=form)


@blueprint.route("/applications/<application_id>/", methods=['GET', 'POST'])
@login_required
def application_view(application_id):
    user_id = current_user.get_id()
    comments = []
    characters = []

    form_app = HrApplicationForm()
    form_comment = HrApplicationCommentForm()

    if AuthInfoManager.get_or_create(current_user.get_id()):
        auth_info = AuthInfoManager.get_or_create(current_user.get_id())

    if HrApplication.query.filter_by(id=int(application_id)).first():
        application = HrApplication.query.filter_by(id=int(application_id)).first()

        if current_user.has_role("recruiter") or current_user.has_role("admin"):
            characters = EveCharacter.query.filter_by(user_id=application.user_id).all()

            comments = HrApplicationComment.query.filter_by(application_id=application_id).all()

        # if HrManager.check_if_application_owned_by_user(application_id, user_id):
        #     form_app.how_long.data = application.how_long
        #     form_app.have_done.data = application.have_done
        #     form_app.scale.data = application.scale
        #     form_app.reason_for_joining.data = application.reason_for_joining
        #     form_app.favorite_ship.data = application.favorite_ship
        #     form_app.favorite_role.data = application.favorite_role
        #     form_app.most_fun.data = application.most_fun
        #     for character in EveCharacter.query.filter_by(user_id=application.user_id).all():
        #          character_choices = character_choices + [(character.character_id, character.character_name)]
        #
        #     form_app.characters.data = application.characters
        #     form_app.characters.choices = character_choices
        #
        #     if request.method == 'POST':
        #         HrManager.update_application(how_long=form_app.how_long.data,
        #                                  have_done=form_app.have_done.data,
        #                                  scale=form_app.scale.data,
        #                                  reason_for_joining=form_app.reason_for_joining.data,
        #                                  favorite_ship=form_app.favorite_ship.data,
        #                                  favorite_role=form_app.favorite_role.data,
        #                                  most_fun=form_app.most_fun.data,
        #                                  application_id=application.id,
        #                                  main_character_name=current_user.auth_info[0].main_character.character_name,
        #                                  user_id=user_id)

        if HrManager.check_if_application_owned_by_user(application_id, user_id) or current_user.has_role("recruiter") or current_user.has_role("admin"):
            return render_template('recruit/application.html',
                                       auth_info=auth_info,
                                       current_user=current_user,
                                       application=application,
                                       characters=characters,
                                       comments=comments,
                                       form_comment=form_comment,
                                       form_app=form_app)

    return redirect(url_for('recruit.applications'))


@blueprint.route("/applications/<application_id>/comment/", methods=['POST'])
@login_required
def application_comment_create(application_id):
    user_id = current_user.get_id()
    form_comment = HrApplicationCommentForm()

    if current_user.has_role("recruiter") or current_user.has_role("admin"):

        if HrApplication.query.filter_by(id=int(application_id)).first():

            if request.method == 'POST':

                if form_comment.validate_on_submit():
                    application = HrApplication.query.filter_by(id=int(application_id)).first()

                    HrManager.create_comment(application_id, form_comment.comment.data, user_id)

                    if application.approved_denied == "Pending":
                        application.approved_denied = "Undecided"
                        application.save()

                    return redirect(url_for('recruit.application_view', application_id=application_id))

            return redirect(url_for('recruit.application_view', application_id=application_id))

    return redirect(url_for('recruit.applications'))

@blueprint.route("/applications/<application_id>/comment/<comment_id>/<action>", methods=['GET', 'POST'])
@login_required
def application_comment_action(application_id, comment_id, action):
    user_id = current_user.get_id()
    form_comment = HrApplicationCommentForm()

    if current_user.has_role("recruiter") or current_user.has_role("admin"):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            if HrApplicationComment.query.filter_by(id=comment_id).first():

                comment = HrApplicationComment.query.filter_by(id=comment_id).first()

                if str(comment.user_id) == str(user_id) or current_user.has_role("admin"):

                    if request.method == 'POST' and action == "edit":
                        flash("request method if", category="message")
                        if form_comment.validate_on_submit():
                            flash("comment valid", category="message")
                            comment.comment = form_comment.comment.data
                            comment.save()

                    elif action == "delete":
                        comment.delete()

            return redirect(url_for('recruit.application_view', application_id=application_id))

    return redirect(url_for('recruit.applications'))


@blueprint.route("/applications/<application_id>/<action>", methods=['GET', 'POST'])
@login_required
def application_interact(application_id, action):
    user_id = current_user.get_id()
    comments = []

    if AuthInfoManager.get_or_create(current_user.get_id()):
        auth_info = AuthInfoManager.get_or_create(current_user.get_id())
        if auth_info.main_character_id == None:
            return redirect(url_for('user.eve_characters'))

    if HrApplication.query.filter_by(id=int(application_id)).first():
        application = HrApplication.query.filter_by(id=int(application_id)).first()

        # alter_application takes one of 4 actions
        if current_user.has_role("admin") or current_user.has_role("recruiter"):
            application_status = HrManager.alter_application(application_id, action, user_id)
            print application.user.auth_info[0].main_character
            flash("%s's application %s" % (application.user.auth_info[0].main_character, application_status), category='message')

        elif application.user_id == user_id:
            if action == "delete" and application.approve_deny == "Pending":
                application_status = HrManager.alter_application(application_id, action, user_id)
                flash("%s's application %s" % (application.main_character, application_status), category='message')

        if application_status and application_status != "deleted":
            return redirect(url_for('recruit.application_view', application_id=application.id))

    return redirect(url_for('recruit.applications'))

