from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField,\
    SubmitField, SelectField, TextAreaField, StringField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


# A custom validator for not requiring data if the passed in field is false
class RequiredIfNot(object):
    # a validator which makes a field required if another field is set and has a truthy value
    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if not bool(other_field.data):
            if not field.data:
                raise ValidationError('Field is required') 


class HrApplicationForm(Form):

    characters = SelectMultipleField(label="Characters which are applying",
        validators=[DataRequired()], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    alt_application = BooleanField(label="Is this an application for an alt?, leave unchecked if you're not sure")

    thesis                  = TextAreaField("KarmaFleet is a new player corporation. If you started playing EVE more than 6 months ago, why are you looking to join a new player corporation? If you are new, what made you want to play EVE in the first place?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    how_long                = TextAreaField("How long have you been playing EVE?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    notable_accomplishments = TextAreaField("Any notable accomplishments in that time?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    corporation_history     = TextAreaField("Walk us through your Corporation history:",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    why_leaving             = TextAreaField("Why are you leaving your current Corporation?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    what_know               = TextAreaField("What do you know about KarmaFleet",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    what_expect             = TextAreaField("How do you expect daily life in KarmaFleet to be?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    bought_characters       = TextAreaField("Do you have any other accounts or characters? Are any of your characters bought, and if so, which ones?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    why_interested          = TextAreaField("Why are you interested in joining KarmaFleet?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    goon_interaction        = TextAreaField("Have you ever interacted with another member of Goonswarm Federation?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    friends                 = TextAreaField("Do you have any friends in KarmaFleet? If so, who?",
                                validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])

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
                                 ('10 (Pure PVP)', '10 (Pure PVP)')])

    favorite_role = TextAreaField("What's your favorite role to play, why?",
                        validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])
    find_out      = TextAreaField("How did you find out about KarmaFleet?",
                        validators=[RequiredIfNot('alt_application'), Length(min=-1, max=2000, message='Max length %(max)d')])

    recaptcha = RecaptchaField()

    submit = SubmitField(label='Submit Application')


class HrApplicationCommentForm(Form):
    comment = TextAreaField(label="New Comment", validators=[DataRequired()])
    submit = SubmitField(label='Add Comment')
    
class HrApplicationCommentEdit(Form):
    comment = TextAreaField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label='Save')

class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField(label='Submit')
