from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted

from recruit_app.user.managers import EveManager, AuthInfoManager
from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, User
from recruit_app.recruit.models import HrApplication, HrApplicationComment
from recruit_app.recruit.managers import HrManager
from recruit_app.recruit.forms import HrApplicationForm, HrApplicationCommentForm, SearchForm

import datetime as dt

blueprint = Blueprint("recruit", __name__, url_prefix='/recruits',
                        static_folder="../static")

@blueprint.route("/applications/", methods=['GET', 'POST'])
@blueprint.route("/applications/<int:page>", methods=['GET', 'POST'])
@login_required
def applications(page=1):
    auth_info = AuthInfoManager.get_or_create(current_user)

    query = HrApplication.query.filter(HrApplication.hidden == False,
                                       HrApplication.user_id == current_user.get_id())
    personal_applications = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('recruit/applications.html',
                           personal_applications=personal_applications)


@blueprint.route("/application_queue/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def application_queue(page=1):
    search_results = []

    search_form = SearchForm()

    query = HrApplication.query.filter(HrApplication.hidden == False,
                                       (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided")).order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            #search_results = HrApplication.query.whoosh_search(search_form.search.data + '*')
            recruiter_queue = HrApplication.query.whoosh_search(search_form.search.data + '*').paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form)


@blueprint.route("/application_queue/all/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def application_all(page=1):
    search_results = []

    search_form = SearchForm()

    query = HrApplication.query.filter(HrApplication.hidden == False,
                                       (HrApplication.approved_denied == "Pending") | (HrApplication.approved_denied == "Undecided")).order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            search_results = query.whoosh_search(search_form.search.data + "*")
            recruiter_queue = search_results.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form,
                           search_results=search_results)



@blueprint.route("/application_queue/history/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/history/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def application_history(page=1):
    search_results = []

    search_form = SearchForm()

    query = HrApplication.query.filter(HrApplication.hidden == False).order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            search_results = HrApplication.query.whoosh_search(search_form.search.data + "*")
            recruiter_queue = search_results.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form,
                           search_results=search_results)


@blueprint.route("/applications/create", methods=['GET', 'POST'])
@login_required
def application_create():
    auth_info = AuthInfoManager.get_or_create(current_user)

    form = HrApplicationForm()

    characters = EveCharacter.query.filter_by(user_id=current_user.get_id()).all()
    character_choices = []
    for character in characters:
        character_choices = character_choices + [(character.character_id, character.character_name)]

    form.characters.choices = character_choices

    if request.method == 'POST':
        if form.validate_on_submit():
            application = HrManager.create_application(form,
                                                       main_character_name=current_user.auth_info[0].main_character.character_name,
                                                       user=current_user)

            flash("Application Created, apply in game with \"" + url_for('recruit.application_view', _external=True, application_id=application.id) + "\" in the body", category='message')
            return redirect(url_for('recruit.application_view', application_id=application.id))

    return render_template('recruit/application_create.html',
                           form=form)


@blueprint.route("/application/<int:application_id>/", methods=['GET', 'POST'])
@login_required
def application_view(application_id):
    comments = []
    characters = []

    form_app = HrApplicationForm()
    form_comment = HrApplicationCommentForm()

    application = HrApplication.query.filter_by(id=application_id).first()
    if application:
        if current_user.has_role("recruiter") or current_user.has_role("admin"):
            characters = EveCharacter.query.filter_by(user_id=application.user_id).all()

            comments = HrApplicationComment.query.filter_by(application_id=application_id).all()

            return render_template('recruit/application.html',
                                   application=application,
                                   characters=characters,
                                   comments=comments,
                                   form_comment=form_comment,
                                   form_app=form_app)

        elif int(application.user_id) == int(current_user.get_id()):

            return render_template('recruit/application.html',
                                   application=application,
                                   characters=characters,
                                   comments=comments,
                                   form_comment=form_comment,
                                   form_app=form_app)

    return redirect(url_for('recruit.applications'))


@blueprint.route("/applications/<application_id>/comment/", methods=['POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def application_comment_create(application_id):
    form_comment = HrApplicationCommentForm()

    application = HrApplication.query.filter_by(id=int(application_id)).first()

    if application:
        if request.method == 'POST':

            if form_comment.validate_on_submit():

                HrManager.create_comment(application, form_comment.comment.data, current_user)

                if application.approved_denied == "Pending":
                    application.approved_denied = "Undecided"
                    application.save()

        return redirect(url_for('recruit.application_view', application_id=application_id))

    return redirect(url_for('recruit.applications'))

@blueprint.route("/applications/<int:application_id>/comment/<int:comment_id>/<action>/", methods=['GET', 'POST'])
@login_required
def application_comment_action(application_id, comment_id, action):
    form_comment = HrApplicationCommentForm()

    if current_user.has_role("recruiter") or current_user.has_role("admin"):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            if HrApplicationComment.query.filter_by(id=comment_id).first():

                comment = HrApplicationComment.query.filter_by(id=comment_id).first()

                if comment.user_id == current_user.get_id() or current_user.has_role("admin"):

                    if request.method == 'POST':
                        if action == "edit":
                            if form_comment.validate_on_submit():
                                flash("comment valid", category="message")
                                HrManager.edit_comment(comment, form_comment.comment.data)

                        elif action == "delete":
                            print "wat"
                            comment.delete()

                    elif action == "delete":
                        print "wat"
                        comment.delete()
            return redirect(url_for('recruit.application_view', application_id=application_id))

    return redirect(url_for('recruit.applications'))


@blueprint.route("/applications/<int:application_id>/<action>", methods=['GET', 'POST'])
@login_required
def application_interact(application_id, action):
    application_status = None

    auth_info = AuthInfoManager.get_or_create(current_user)

    if auth_info.main_character_id == None:
        return redirect(url_for('user.eve_characters'))

    application = HrApplication.query.filter_by(id=application_id).first()
    if application:
        # alter_application takes one of 4 actions
        if current_user.has_role("admin") or current_user.has_role("recruiter"):
            if current_user.has_role("admin") or action != "delete":
                application_status = HrManager.alter_application(application, action, current_user)

                flash("%s's application %s" % (application.main_character_name,
                                               application_status),
                      category='message')

        elif application.user_id == current_user.get_id():
            if action == "delete" and application.approve_deny == "Pending":
                application_status = HrManager.alter_application(application, action, current_user)
                flash("%s's application %s" % (application.main_character,
                                               application_status),
                      category='message')

        if application_status and application_status != "deleted":
            return redirect(url_for('recruit.application_view',
                                    application_id=application.id))

    return redirect(url_for('recruit.applications'))

