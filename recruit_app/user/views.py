from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.decorators import login_required
from flask_security import current_user

from .managers import EveManager, AuthInfoManager
from .eve_api_manager import EveApiManager
from .forms import UpdateKeyForm

from .models import EveCharacter, EveAllianceInfo, EveApiKeyPair


import datetime as dt

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/members.html")

@blueprint.route("/api_add", methods=['GET', 'POST'])
@login_required
def api_add():
    form = UpdateKeyForm()
    if form.validate_on_submit():
        characters = EveApiManager.get_characters_from_api(form.data['api_id'],
                                                               form.data['api_key'])
        EveManager.create_characters_from_list(characters, current_user.get_id(), form.data['api_id'])

        EveManager.create_corporations_from_list(characters)

        EveManager.create_alliances_from_list(characters)

        EveManager.create_api_keypair(form.data['api_id'],
                                          form.data['api_key'],
                                          current_user.get_id())

        return redirect(url_for('user.api_manage'))
    else:
        return render_template("users/api_add.html", form=form)


@blueprint.route("/api_manage", methods=['GET', 'POST'])
@login_required
def api_manage():
    context = {'apikeypairs': EveManager.get_api_key_pairs(current_user.get_id())}

    return render_template("users/api_manage.html", context=context)


@blueprint.route("/api_delete/<api_id>", methods=['GET', 'POST'])
@login_required
def api_delete(api_id):
    authinfo = AuthInfoManager.get_or_create(current_user.get_id())
    # Check if our users main id is in the to be deleted characters
    characters = EveManager.get_characters_by_owner_id(current_user.get_id())
    if characters is not None:
        for character in characters:
            if character.character_id == authinfo.main_character_id:
                if character.api_id == api_id:
                    #TODO disable services and such
                    pass

    EveManager.delete_api_key_pair(api_id, current_user.get_id())
    EveManager.delete_characters_by_api_id(api_id, current_user.get_id())

    return redirect(url_for('user.api_manage'))

@blueprint.route("/api_update/<api_id>", methods=['GET', 'POST'])
@login_required
def api_update(api_id):
    if EveApiKeyPair.query.filter_by(api_id=api_id).first():
        api_key_pair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
        if unicode(api_key_pair.user_id) == unicode(current_user.get_id()):
            if (dt.datetime.now() - api_key_pair.last_update_time).total_seconds() >= 30:
                EveManager.update_api_keypair(api_id=api_key_pair.api_id, api_key=api_key_pair.api_key)
                return redirect(url_for('user.api_manage'))
            else:
                flash("Please Wait before refreshing your api", category='message')
                return redirect(url_for('user.api_manage'))
        else:
            return redirect(url_for('user.api_manage'))

    return redirect(url_for('user.api_manage'))

@blueprint.route("/eve_characters", methods=['GET', 'POST'])
@login_required
def eve_characters():
    characters = []
    authinfo = []
    if EveManager.get_characters_by_owner_id(current_user.get_id()):
        # characters = EveManager.get_characters_by_owner_id(current_user.get_id())
        characters = EveManager.get_characters_by_owner_id(current_user.get_id())

    if AuthInfoManager.get_or_create(current_user.get_id()):
        authinfo = AuthInfoManager.get_or_create(current_user.get_id())
    return render_template('users/eve_characters.html', characters=characters, authinfo=authinfo)

@blueprint.route("/eve_main_character_change/<character_id>", methods=['GET', 'POST'])
@login_required
def eve_main_character_change(character_id):
    if EveManager.check_if_character_owned_by_user(character_id, current_user.get_id()):
        AuthInfoManager.update_main_character_id(character_id, current_user.get_id())
        return redirect(url_for('user.eve_characters'))
    return redirect(url_for('user.eve_characters'))


