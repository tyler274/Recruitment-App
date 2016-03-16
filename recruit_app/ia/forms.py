from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SubmitIssueForm(Form):

    subject = StringField("Subject", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    logs = TextAreaField("Applicable Chat Logs")

    submit = SubmitField(label='Submit Issue')
