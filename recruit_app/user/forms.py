from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User

from .managers import EveManager
from .eve_api_manager import EveApiManager

class RegisterForm(Form):
    username = StringField(label=u'Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(label=u'Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField(label=u'Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(label=u'Verify password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(u'Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(u'Email already registered')
            return False
        return True

class UpdateKeyForm(Form):
    api_id = StringField(label=u'Key ID', validators=[DataRequired(), Length(min=1, max=10)])
    api_key = StringField(label=u'Verification Code', validators=[DataRequired(), Length(min=1, max=254)])
    submit = SubmitField(label=u'Submit')

    def validate(self):
        initial_validation = super(UpdateKeyForm, self).validate()
        if not initial_validation:
            return False
        if EveManager.check_if_api_key_pair_exist(self.api_id.data):
            self.api_id.errors.append(u'API key already exists')
            return False

        if not EveApiManager.check_api_is_type_account(self.api_id.data,
                                                       self.api_key.data):
            self.api_id.errors.append(u'API not of type account')
            return False

        if not EveApiManager.check_api_is_full(self.api_id.data,
                                               self.api_key.data):
            self.api_id.errors.append(u'API supplied is not a full api key')
            return False
        if not EveApiManager.check_api_is_not_expire(self.api_id.data,
                                                     self.api_key.data):
            self.api_id.errors.append(u'API supplied is not forever')
            return False
        return True


