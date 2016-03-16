from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_security.decorators import login_required
from flask_security import current_user

from recruit_app.ia.managers import IaManager
from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.ia.forms import SubmitIssueForm

blueprint = Blueprint("ia", __name__, url_prefix='/ia', static_folder="../static")

@blueprint.route("/submit_issue", methods=['GET', 'POST'])
@login_required
def submit_issue():
    # Check if user is in Karmafleet (98370861)
    if not EveApiManager.check_if_character_is_in_corp(int(current_user.main_character_id), 98370861):
        flash('You are not a current KarmaFleet member.', 'error')
        return redirect(url_for('public.home'))
        
    form = SubmitIssueForm()
       
    # Display for if get, submit if POST
    if request.method == 'POST':
        if form.validate_on_submit():
        # Do the submission
            if IaManager.submit_issue(current_user, form.subject.data, form.body.data, form.logs.data):
                flash('Issue submitted successfully.', 'info')
            else:
                flash('Error submitting issue.  Please try again later.', 'error')
            return redirect(url_for('public.home'))
        
    # GET
    return render_template('ia/submit_issue.html', form=form)