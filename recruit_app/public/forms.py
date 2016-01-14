from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from recruit_app.user.models import User

from recruit_app.extensions import user_datastore

from flask_security.forms import ConfirmRegisterForm, PasswordConfirmFormMixin


class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = user_datastore.get_user(self.email.data)
        if not self.user:
            self.email.errors.append('Unknown email address')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.email.errors.append('User not activated')
            return False
        return True


class ConfirmRegisterFormRecaptcha(ConfirmRegisterForm, PasswordConfirmFormMixin):
    recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        super(ConfirmRegisterForm, self).__init__(*args, **kwargs)
