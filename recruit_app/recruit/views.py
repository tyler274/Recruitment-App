from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted
from recruit_app.extensions import cache

from recruit_app.user.managers import AuthInfoManager

from recruit_app.user.models import EveCharacter
from recruit_app.recruit.models import HrApplication, HrApplicationComment
from recruit_app.recruit.managers import HrManager
from recruit_app.recruit.forms import HrApplicationForm, HrApplicationCommentForm, HrApplicationCommentEdit, SearchForm
from recruit_app.blacklist.models import BlacklistCharacter

from sqlalchemy import desc, asc

import requests
from bs4 import BeautifulSoup

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

@blueprint.route("/compliance/", methods=['GET'])
@login_required
@roles_accepted('admin', 'compliance')
def compliance():
    return render_template('recruit/compliance.html', data=HrManager.get_compliance())


@blueprint.route("/application_queue/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer')
def application_queue(page=1):
    search_results = []
    # from recruit_app.database import Model
    # from recruit_app.extensions import db
    # #current_app.config['SQLALCHEMY_ECHO'] = True
    # db.configure_mappers()
    #
    # HrApplication.metadata.create_all(db.session.connection())
    #
    # db.session.commit()

    search_form = SearchForm()

    query = HrApplication.query\
        .filter(HrApplication.hidden == False,
                (HrApplication.approved_denied == "New")
                | (HrApplication.approved_denied == "Undecided")
                | (HrApplication.approved_denied == "Role Stasis")
                | (HrApplication.approved_denied == "Awaiting Response")
                | (HrApplication.approved_denied == "Needs Processing")
                | (HrApplication.approved_denied == "Needs Director Review"))\
        .order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if search_form.validate_on_submit():

            #search_results = HrApplication.query.search(unicode(search_form.search.data))
            #print search_results
            #recruiter_queue = search_results.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)
            # print recruiter_queue.items
            # recruiter_queue = HrApplication\
            #     .query\
            #     .whoosh_search('*' + str(search_form.search.data) + '*')\
            #     .paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)
            recruiter_queue = HrApplication.query.join(EveCharacter, EveCharacter.user_id == HrApplication.user_id).filter(EveCharacter.character_name.ilike("%" + str(search_form.search.data)  + "%")).paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)
    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form)


@blueprint.route("/application_queue/all/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer')
def application_all(page=1):
    search_results = []

    search_form = SearchForm()

    query = HrApplication.query\
        .filter(HrApplication.hidden == False,
                (HrApplication.approved_denied == "New")
                | (HrApplication.approved_denied == "Undecided")
                | (HrApplication.approved_denied == "Role Stasis")
                | (HrApplication.approved_denied == "Awaiting Response")
                | (HrApplication.approved_denied == "Needs Director Review"))\
        .order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, len(query.all()), False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            # search_results = query.whoosh_search(search_form.search.data + "*")
            search_results = HrApplication.query.join(EveCharacter, EveCharacter.user_id == HrApplication.user_id).filter(EveCharacter.character_name.ilike("%" + str(search_form.search.data)  + "%"))
            recruiter_queue = search_results.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('recruit/application_queue.html',
                           recruiter_queue=recruiter_queue,
                           search_form=search_form,
                           search_results=search_results)



@blueprint.route("/application_queue/history/", methods=['GET', 'POST'])
@blueprint.route("/application_queue/history/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer')
def application_history(page=1):
    search_results = []

    search_form = SearchForm()

    query = HrApplication.query.filter(HrApplication.hidden == False).order_by(HrApplication.id)

    recruiter_queue = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if search_form.validate_on_submit():
            # search_results = HrApplication.query.whoosh_search(search_form.search.data + "*")
            # recruiter_queue = search_results.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)
            recruiter_queue = HrApplication.query.join(EveCharacter, EveCharacter.user_id == HrApplication.user_id).filter(EveCharacter.character_name.ilike("%" + str(search_form.search.data)  + "%")).paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

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


@blueprint.route("/applications/<int:application_id>/", methods=['GET', 'POST'])
@login_required
def application_view(application_id):
    comments = []
    characters = []

    form_app = HrApplicationForm()
    form_comment = HrApplicationCommentForm()
    form_edit = HrApplicationCommentEdit()

    application = HrApplication.query.filter_by(id=application_id).first()
    if application:
        if current_user.has_role("recruiter") or current_user.has_role("admin") or current_user.has_role('reviewer'):
            blacklist_ips = list(set([x.ip_address for x in BlacklistCharacter.query.all() if x.ip_address is not None and x.ip_address is not u'']))
            ips = [i for e in blacklist_ips for i in application.user.get_ips() if e in i]
            if len(ips) > 0:
                flash("Heads up this person's IP is on the blacklist:" + unicode(ips))
            else:
                flash("No IP's found on blacklist")

            characters = EveCharacter.query.filter_by(user_id=application.user_id).all()

            comments = HrApplicationComment.query.filter_by(
                application_id=application_id)\
                .order_by(asc(HrApplicationComment.created_time))\
                .all()
                
            gsf_blacklist = {}
            for character in characters:
                gsf_blacklist[character.character_name] = "UNKNOWN"
                
            gsf_blacklist_str = ''
            try:
            
                for character in characters:
                    url = current_app.config['GSF_BLACKLIST_URL'] + character.character_name
                    r   = requests.post(url)
                    result = str(r.json()[0]['output'])
                    gsf_blacklist[character.character_name] = result
                    if (result == 'BLACKLISTED'):
                        gsf_blacklist_str += character.character_name + ' '
            except:
                pass
                
            if len(gsf_blacklist_str) > 0:
                flash("WARNING - Character(s) " + unicode(gsf_blacklist_str) + "are on the GSF blacklist!")

            blacklist_string = ''
            try:
                for character in characters:
                    blacklist_string = blacklist_string + ' ' + str(character.character_name)

                # blacklist_query = BlacklistCharacter\
                #     .query\
                #     .whoosh_search(blacklist_string, or_=True).all()
                query = BlacklistCharacter.query.filter(BlacklistCharacter.name.in_([x.character_name for x in characters])).all()

                if query:
                    flash('Double check blacklist, ' + str(query) + ' matched')
                else:
                    flash('No blacklist entries found')
            finally:
                pass

            return render_template('recruit/application.html',
                                   application=application,
                                   characters=characters,
                                   comments=comments,
                                   form_comment=form_comment,
                                   form_edit=form_edit,
                                   form_app=form_app,
                                   gsf_blacklist=gsf_blacklist)

        elif int(application.user_id) == int(current_user.get_id()):

            return render_template('recruit/application.html',
                                   application=application,
                                   form_app=form_app)

    return redirect(url_for('recruit.applications'))


@blueprint.route("/applications/<application_id>/comment/", methods=['POST'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer')
def application_comment_create(application_id):
    form_comment = HrApplicationCommentForm()

    application = HrApplication.query.filter_by(id=int(application_id)).first()

    if application:
        if request.method == 'POST':
            if form_comment.validate_on_submit():
                HrManager.create_comment(application, form_comment.comment.data, current_user)

        return redirect(url_for('recruit.application_view', application_id=application_id))

    return redirect(url_for('recruit.applications'))

@blueprint.route("/applications/<int:application_id>/comment/<int:comment_id>/<action>/", methods=['GET', 'POST'])
@login_required
def application_comment_action(application_id, comment_id, action):
    form_edit = HrApplicationCommentForm()
    
    if current_user.has_role("recruiter") or current_user.has_role("admin") or current_user.has_role('reviewer'):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            if HrApplicationComment.query.filter_by(id=comment_id).first():

                comment = HrApplicationComment.query.filter_by(id=comment_id).first()

                if int(comment.user_id) == int(current_user.get_id()) or current_user.has_role("admin"):
                    if request.method == 'POST':
                        if action == "edit":
                            if form_edit.validate_on_submit():
                                HrManager.edit_comment(comment, form_edit.comment.data, current_user.get_id())

                        elif action == "delete":
                            comment.delete()

                    elif action == "delete":
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
        if current_user.has_role('admin') or current_user.has_role('recruiter') or current_user.has_role('reviewer'):
            if current_user.has_role("admin") or (action not in ['delete', 'hide', 'unhide']):
                if current_user.has_role('recruiter') or current_user.has_role('admin') or (action not in ['approve', 'reject', 'close']):
                    application_status = HrManager.alter_application(application, action, current_user)

                    flash("%s's application %s" % (application.main_character_name,
                                                   application_status),
                          category='message')

        elif application.user_id == current_user.get_id():
            if action == "delete" and application.approve_deny == "New":
                application_status = HrManager.alter_application(application, action, current_user)
                flash("%s's application %s" % (application.main_character,
                                               application_status),
                      category='message')

        if application_status and application_status != "deleted":
            return redirect(url_for('recruit.application_view',
                                    application_id=application.id))

    return redirect(url_for('recruit.applications'))

