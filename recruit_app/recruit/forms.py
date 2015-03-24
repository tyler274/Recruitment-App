from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from recruit_app.user.models import User

from recruit_app.user.managers import EveManager
from recruit_app.user.eve_api_manager import EveApiManager




