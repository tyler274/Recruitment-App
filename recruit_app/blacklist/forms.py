from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField,\
    SubmitField, SelectField, TextAreaField, StringField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField(label='Submit')


class BlacklistCharacterForm(Form):
    character_name = TextAreaField("Character Name",
                                validators=[Length(min=-1, max=2000, message='Max length %(max)d')])

    main_name = TextAreaField("Main Name",
                                validators=[Length(min=-1, max=2000, message='Max length %(max)d')])

    corporation = TextAreaField("Corporation",
                             validators=[DataRequired(), Length(min=-1,
                                                                max=2000,
                                                                message='Max length %(max)d')])

    alliance = TextAreaField("Alliance", validators=[DataRequired(), Length(min=-1,
                                                                            max=2000,
                                                                            message='Max length %(max)d')])
    notes = TextAreaField("Notes", validators=[DataRequired(), Length(min=-1,
                                                                      max=2000,
                                                                      message='Max length %(max)d')])

    submit = SubmitField(label='Submit Entry')



