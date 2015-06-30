import flask_whooshalchemy as whooshalchemy

from models import BlacklistCharacter

def register_search_models(app):
    whooshalchemy.whoosh_index(app, BlacklistCharacter)