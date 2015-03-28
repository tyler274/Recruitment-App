import flask_whooshalchemy as whooshalchemy

from models import HrApplication, HrApplicationComment

def register_search_models(app):
    whooshalchemy.whoosh_index(app, HrApplication)