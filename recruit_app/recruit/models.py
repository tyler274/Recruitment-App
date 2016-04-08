# -*- coding: utf-8 -*-

from recruit_app.extensions import bcrypt
from recruit_app.database import Column, db, Model, ReferenceCol, relationship, SurrogatePK, TimeMixin
from sqlalchemy.orm import backref

# import flask_whooshalchemy as whooshalchemy
# from sqlalchemy_searchable import make_searchable
# from sqlalchemy_utils.types import TSVectorType, ScalarListType
#
# from sqlalchemy_searchable import SearchQueryMixin
from flask_sqlalchemy import BaseQuery
# from sqlalchemy.dialects import postgresql

import datetime

# make_searchable()


character_apps = db.Table('app_characters',
        db.Column('app_id', db.Integer(), db.ForeignKey('hr_applications.id')),
        db.Column('character_id', db.String(), db.ForeignKey('characters.character_id')))


class HrApplication(SurrogatePK, TimeMixin, Model):
    # query_class = HrApplicationQuery
    __tablename__ = 'hr_applications'

    __searchable__ = ['thesis',
                      'how_long',
                      'notable_accomplishments',
                      'corporation_history',
                      'why_leaving',
                      'what_know',
                      'what_expect',
                      'bought_characters',
                      'why_interested',
                      'find_out',
                      'favorite_role',
                      'main_character_name']

    main_character_name = Column(db.Unicode, nullable=True)

    alt_application = Column(db.Boolean, default=False)

    characters = relationship('EveCharacter', secondary=character_apps, backref=db.backref('hr_applications', lazy='dynamic'), lazy='dynamic')

    thesis = Column(db.UnicodeText, nullable=True)
    how_long = Column(db.Text, nullable=True)
    notable_accomplishments = Column(db.Text, nullable=True)
    corporation_history = Column(db.Text, nullable=True)
    why_leaving = Column(db.Text, nullable=True)
    what_know = Column(db.Text, nullable=True)
    what_expect = Column(db.Text, nullable=True)
    bought_characters = Column(db.Text, nullable=True)
    why_interested = Column(db.Text, nullable=True)

    goon_interaction = Column(db.Text, nullable=True)
    friends = Column(db.Text, nullable=True)

    scale = Column(db.Text, nullable=True)

    find_out = Column(db.Text, nullable=True)

    favorite_role = Column(db.Text, nullable=True)

    user_id = ReferenceCol('users', nullable=True)
    reviewer_user_id = ReferenceCol('users', nullable=True)
    last_user_id = ReferenceCol('users', nullable=True)

    approved_denied = Column(db.Text, default="New")

    hidden = Column(db.Boolean, nullable=True, default=False)

    # search_vector = Column(TSVectorType('main_character_name', 'thesis'))

    user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
    reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
    last_action_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')
    
    training = Column(db.Boolean, default=False)

    def __str__(self):
        return '<Application %r>' % str(self.main_character_name)


class HrApplicationComment(SurrogatePK, TimeMixin, Model):
    __tablename__ = 'hr_comments'

    comment = Column(db.Text, nullable=True)

    application_id = ReferenceCol('hr_applications')
    user_id = ReferenceCol('users')
    application = relationship('HrApplication', foreign_keys=[application_id], backref=backref('hr_comments', cascade="delete"))
    user = relationship('User', backref='hr_comments', foreign_keys=[user_id])

    def __repr__(self):
        return str(self.user) + " - Comment"

class HrApplicationCommentHistory(SurrogatePK, TimeMixin, Model):
    __tablename__ = 'hr_comment_history'
    
    old_comment = Column(db.Text, nullable=True)
    comment_id = ReferenceCol('hr_comments')
    editor = ReferenceCol('users')
    comment = relationship('HrApplicationComment', foreign_keys=[comment_id], backref=backref('hr_comment_history', cascade="delete"))
    user = relationship('User', backref='hr_comment_history', foreign_keys=[editor])
    
    def __repr__(self):
        return str(self.editor) + " - Edited comment"
