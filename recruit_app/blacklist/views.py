from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted

from .forms import SearchForm, BlacklistCharacterForm
from .models import BlacklistCharacter
from .managers import BlacklistManager


blueprint = Blueprint("blacklist", __name__, url_prefix='/blacklist',
                        static_folder="../static")

@blueprint.route("/", methods=['GET', 'POST'])
@blueprint.route("/<int:page>/", methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'recruiter')
def blacklist_view(page=1):
    search_form = SearchForm()
    blacklist_form = BlacklistCharacterForm()
    query = BlacklistCharacter.query

    blacklist = query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    if request.method == 'POST':
        if current_user.has_role('admin'):
            if blacklist_form.validate_on_submit():
                if BlacklistManager.create_entry(blacklist_form, current_user):
                    flash('Entry Added')
        else:
            flash('Not an Admin')
        if search_form.validate_on_submit():
            blacklist = BlacklistCharacter\
                .query\
                .whoosh_search('*' + str(search_form.search.data) + '*')\
                .paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('blacklist/blacklist.html',
                           blacklist=blacklist,
                           search_form=search_form,
                           blacklist_form=blacklist_form)
