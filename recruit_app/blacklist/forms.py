from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField,\
    SubmitField, SelectField, TextAreaField, StringField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, IPAddress, Optional


class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField(label='Submit')


class BlacklistCharacterForm(Form):
    character_name = TextAreaField("Character Name", validators=[Length(min=-1, max=2000, message='Max length %(max)d')])
    main_name      = TextAreaField("Main Name",      validators=[Length(min=-1, max=2000, message='Max length %(max)d')])
    corporation    = TextAreaField("Corporation",    validators=[Length(min=-1, max=2000, message='Max length %(max)d')])
    alliance       = TextAreaField("Alliance",       validators=[Length(min=-1, max=2000, message='Max length %(max)d')])
    ip_address     = TextAreaField("IP Address",     validators=[IPAddress(), Optional()])
    notes          = TextAreaField("Notes",          validators=[Length(min=-1, max=2000, message='Max length %(max)d')])

    submit = SubmitField(label='Submit Entry')
