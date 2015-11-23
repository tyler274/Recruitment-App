from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField,\
    SubmitField, SelectField, TextAreaField, StringField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class HrApplicationForm(Form):

    characters = SelectMultipleField(label="Characters which are applying",
                                     validators=[DataRequired()],
                                     option_widget=widgets.CheckboxInput(),
                                     widget=widgets.ListWidget(prefix_label=False))

    alt_application = BooleanField(label="Is this an application for an alt?, leave unchecked if you're not sure")

    thesis = TextAreaField("Please give a maximum 2000 character thesis on the meaning of the word \"The\" (not required)",
                                validators=[Length(min=-1, max=2000, message='Max length %(max)d')])

    how_long = TextAreaField("How long have you been playing EVE?",
                             validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    notable_accomplishments = TextAreaField("Any notable accomplishments in that time?",
                                            validators=[DataRequired(),
                                                        Length(min=-1, max=2000, message='Max length %(max)d')])
    corporation_history = TextAreaField("Walk us through your Corporation history:",
                                        validators=[DataRequired(),
                                                    Length(min=-1, max=2000, message='Max length %(max)d')])

    why_leaving = TextAreaField("Why are you leaving your current Corporation?",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    what_know = TextAreaField("What do you know about KarmaFleet",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    what_expect = TextAreaField("How do you expect daily life in KarmaFleet to be?",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    bought_characters = TextAreaField("Do you have any alts or other characters? Are any of your characters bought, and if so, which ones?", validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    why_interested = TextAreaField("Why are you interested in joining KarmaFleet?",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    goon_interaction = TextAreaField("Have you ever interacted with another member of Goonswarm Federation?",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    friends = TextAreaField("Do you have any friends in KarmaFleet? If so, who?",
                                validators=[DataRequired(),
                                            Length(min=-1, max=2000, message='Max length %(max)d')])

    scale = SelectField("On a scale from 1 to 10, where 1 is pure PvE and 10 is pure PvP, where do you see yourself?",
                        choices=[('0 (Not Sure)', '0 (Not Sure)'),
                                 ('1 (Pure PVE)', '1 (Pure PVE)'),
                                 ('2', '2'),
                                 ('3', '3'),
                                 ('4', '4'),
                                 ('5 (Equal PVE and PVP)', '5 (Equal PVE and PVP)'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8'),
                                 ('9', '9'),
                                 ('10 (Pure PVP)', '10 (Pure PVP)')],
                        validators=[DataRequired()])

    favorite_role = TextAreaField("What's your favorite role to play, why?",
                                  validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    find_out = TextAreaField("How did you find out about KarmaFleet?",
                             validators=[DataRequired(), Length(min=-1, max=2000, message='Max length %(max)d')])

    recaptcha = RecaptchaField()

    submit = SubmitField(label='Submit Application')


class HrApplicationCommentForm(Form):
    comment = TextAreaField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label='Add Comment')
    
class HrApplicationCommentEdit(Form):
    comment = TextAreaField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label='Save')

class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField(label='Submit')


