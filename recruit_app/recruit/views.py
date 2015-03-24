from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.decorators import login_required
from flask_security import current_user

from recruit_app.user.managers import EveManager, AuthInfoManager
from recruit_app.user.eve_api_manager import EveApiManager
from recruit_app.user.forms import UpdateKeyForm

from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair

import datetime as dt

blueprint = Blueprint("recruit", __name__, url_prefix='/recruits',
                        static_folder="../static")





