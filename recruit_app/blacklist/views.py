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
@roles_accepted('admin', 'recruiter', 'reviewer', 'compliance', 'blacklist')
def blacklist_view(page=1):
    search_form = SearchForm()
    blacklist_form = BlacklistCharacterForm()

    blacklist = None
    
    if request.method == 'POST':
        if request.form['submit'] == 'Submit Entry':
            if current_user.has_role('admin') or current_user.has_role('compliance') or current_user.has_role('blacklist'):
                if blacklist_form.validate_on_submit():
                    if BlacklistManager.create_entry(blacklist_form, current_user):
                        flash('Entry Added')
            else:
                flash("You don't have the proper permissions.")
        elif search_form.validate_on_submit() and search_form.search.data:
            blacklist = BlacklistCharacter.query.filter(
                BlacklistCharacter.name.ilike       ("%" + search_form.search.data + "%")|
                BlacklistCharacter.main_name.ilike  ("%" + search_form.search.data + "%")|
                BlacklistCharacter.corporation.ilike("%" + search_form.search.data + "%")|
                BlacklistCharacter.alliance.ilike   ("%" + search_form.search.data + "%")|
                BlacklistCharacter.notes.ilike      ("%" + search_form.search.data + "%")|
                BlacklistCharacter.ip_address.ilike ("%" + search_form.search.data + "%"))\
                .paginate(1, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    # Do the main query after POST to catch new entries, or ignore search query
    if blacklist is None:
        blacklist = BlacklistCharacter.query.paginate(page, current_app.config['MAX_NUMBER_PER_PAGE'], False)

    return render_template('blacklist/blacklist.html', blacklist=blacklist, search_form=search_form, blacklist_form=blacklist_form)
