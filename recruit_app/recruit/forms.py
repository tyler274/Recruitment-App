from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField,\
    SubmitField, SelectField, TextAreaField, StringField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class HrApplicationForm(Form):

    characters = SelectMultipleField(label="Characters which are applying", validators=[DataRequired()],
                                     option_widget=widgets.CheckboxInput(),
                                     widget=widgets.ListWidget(prefix_label=False))

    alt_app = BooleanField(label="Is this an application for an alt?, leave unchecked if you're not sure")

    how_long = TextAreaField("How long have you been playing EVE?",
                             validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    have_done = TextAreaField("What have you done in that time?",
                              validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    scale = SelectField("On a scale from 1 to 10, where 1 is pure PvE and 10 is pure PvP, where do you see yourself?",
                        choices=[('1', u'1 (Pure PVE)'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', u'5 (Equal PVE and PVP)'),
                                 ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),('10', u'10 (Pure PVP)')],
                        validators=[DataRequired()])

    reason_for_joining = TextAreaField("Reason for Joining?",
                                       validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    favorite_ship = TextAreaField("What's your favorite ship, why?",
                                  validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    favorite_role = TextAreaField("What's your favorite role to play, why?",
                                  validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    most_fun = TextAreaField("What's the most fun you've ever had in EVE?",
                             validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    recaptcha = RecaptchaField()

    submit = SubmitField(label='Submit')


class HrApplicationCommentForm(Form):
    comment = TextAreaField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label='Add Comment')

class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField(label='Submit')


