from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User

from .managers import EveManager
from .eve_api_manager import EveApiManager

class RegisterForm(Form):
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class UpdateKeyForm(Form):
    api_id = TextField("Key ID", validators=[DataRequired(), Length(min=1, max=10)])
    api_key = TextField("Verification Code", validators=[DataRequired(), Length(min=1, max=254)])
    submit = SubmitField(label='Submit')

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
        return True


