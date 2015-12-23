from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.decorators import login_required
from flask_security import current_user

from recruit_app.user.managers import EveManager
from recruit_app.user.eve_api_manager import EveApiManager
from recruit_app.user.forms import UpdateKeyForm

from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair

import datetime as dt

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return redirect(url_for('public.home'))

@blueprint.route("/api_add", methods=['GET', 'POST'])
@login_required
def api_add():
    form = UpdateKeyForm()
    if form.validate_on_submit():
        characters = EveApiManager.get_characters_from_api(form.data['api_id'],
                                                               form.data['api_key'])

        if EveManager.create_api_keypair(form.data['api_id'],
                                          form.data['api_key'],
                                          current_user.get_id()):
            EveManager.create_alliances_from_list(characters)
            EveManager.create_corporations_from_character_list(characters)

            character_creation = EveManager.create_characters_from_list(characters, current_user, form.data['api_id'])
            if character_creation:
                flash(character_creation, category="message")
            # else:
            #     flash("Character error, RIP. (contact IT)", category="message")
        else:
            flash("API Key already in use", category='message')
            return render_template("users/api_add.html", form=form)

        return redirect(url_for('user.api_manage'))

    else:
        return render_template("users/api_add.html", form=form)


@blueprint.route("/api_manage", methods=['GET', 'POST'])
@login_required
def api_manage():
    api_key_pairs = EveManager.get_api_key_pairs(current_user)

    return render_template("users/api_manage.html", api_key_pairs=api_key_pairs)


@blueprint.route("/api_delete/<api_id>", methods=['GET', 'POST'])
@login_required
def api_delete(api_id):
    # Check if our users main id is in the to be deleted characters
    characters = EveManager.get_characters_by_owner(current_user)
    if characters is not None:
        for character in characters:
            if character.api_id == api_id and character.character_id == current_user.main_character_id:
                # TODO disable services and such
                pass

    EveManager.delete_characters_by_api_id_user(api_id, current_user)
    EveManager.delete_api_key_pair(api_id, current_user)

    return redirect(url_for('user.api_manage'))

@blueprint.route("/api_update/<api_id>", methods=['GET', 'POST'])
@login_required
def api_update(api_id):
    # Break out application logic from the view to the manager
    update = EveManager.update_user_api(api_id, current_user)

    if update == "Wait":
        flash(u'Please wait before refreshing your api', category='message')
    elif update == "Success":
        flash(u'API key Refreshed', category='message')
    elif update == "Failed":
        flash(u'Error updating API key!  Either your key is invalid or the CCP servers are temporarily down.', category='error')

    return redirect(url_for('user.api_manage'))

@blueprint.route("/eve_characters", methods=['GET', 'POST'])
@login_required
def eve_characters():

    characters = EveCharacter.query.filter_by(user_id=current_user.get_id()).all()

    return render_template('users/eve_characters.html', characters=characters)

@blueprint.route("/eve_main_character_change/<character_id>", methods=['GET', 'POST'])
@login_required
def eve_main_character_change(character_id):
    if EveManager.check_if_character_owned_by_user(character_id, current_user.get_id()):
        current_user.main_character_id = character_id
        current_user.save()

    return redirect(url_for('user.eve_characters'))


