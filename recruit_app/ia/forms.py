from flask_wtf import Form
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SubmitIssueForm(Form):

    subject = TextAreaField("Subject", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    logs = TextAreaField("Applicable Chat Logs")

    submit = SubmitField(label='Submit Issue')
