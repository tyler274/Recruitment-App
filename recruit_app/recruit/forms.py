from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, SelectField, TextAreaField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from recruit_app.user.models import User

from recruit_app.user.managers import EveManager
from recruit_app.user.eve_api_manager import EveApiManager

class HrApplicationForm(Form):
    how_long = TextAreaField("How long have you been playing EVE?", validators=[DataRequired()])

    have_done = TextAreaField("What have you done in that time?", validators=[DataRequired()])

    scale = SelectField("On a scale from 1 to 10, where 1 is pure PvE and 10 is pure PvP, where do you see yourself?", choices=[('1','1'),('2','2'),('3','3'),(
                                '4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')] , validators=[DataRequired()])

    reason_for_joining = TextAreaField("Reason for Joining?", validators=[DataRequired()])

    favorite_ship = TextAreaField("What's your favorite ship, why?", validators=[DataRequired()])

    favorite_role = TextAreaField("What's your favorite role to play, why?", validators=[DataRequired()])

    most_fun = TextAreaField("What's the most fun you've ever had in EVE?", validators=[DataRequired()])

    submit = SubmitField(label='Submit')

class HrApplicationCommentForm(Form):
    comment = TextAreaField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label='Add Comment')

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


