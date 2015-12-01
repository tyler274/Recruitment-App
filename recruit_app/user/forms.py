from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User

from .managers import EveManager
from .eve_api_manager import EveApiManager


class UpdateKeyForm(Form):
    api_id = StringField(label='Key ID', validators=[DataRequired(), Length(min=1, max=10)])
    api_key = StringField(label='Verification Code', validators=[DataRequired(), Length(min=1, max=254)])
    submit = SubmitField(label='Submit')

    def validate(self):
        initial_validation = super(UpdateKeyForm, self).validate()
        if not initial_validation:
            return False
        if EveManager.check_if_api_key_pair_exist(self.api_id.data):
            self.api_id.errors.append(u'API key already registered with this site')
            return False

        if not EveApiManager.check_api_is_type_account(self.api_id.data,
                                                       self.api_key.data):
            self.api_id.errors.append(u'API key is not an account wide API. Select \"All\" as the character when creating the API key.')
            return False

        if not EveApiManager.check_api_is_full(self.api_id.data,
                                               self.api_key.data):
            self.api_id.errors.append(u'API key is not a full API key. Select all items in all categories when creating the key, or use the provided \"Create a full API key\" button to preselect the correct items.')
            return False
        if not EveApiManager.check_api_is_not_expire(self.api_id.data,
                                                     self.api_key.data):
            self.api_id.errors.append(u'API key has an expiry date. Please select the "No Expiry" box when creating the API key.')
            return False
        return True


