# -*- coding: utf-8 -*-
import datetime as dt

from recruit_app.extensions import bcrypt
from recruit_app.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

import flask_whooshalchemy as whooshalchemy
# from sqlalchemy_searchable import make_searchable
# from sqlalchemy_utils.types import TSVectorType
#
# from sqlalchemy_searchable import SearchQueryMixin
# from flask_sqlalchemy import BaseQuery



character_apps = db.Table('app_characters',
        db.Column('app_id', db.Integer(), db.ForeignKey('hr_applications.id')),
        db.Column('character_id', db.String(), db.ForeignKey('characters.character_id')))


# class HrApplicationQuery(BaseQuery, SearchQueryMixin):
#     pass


class HrApplication(SurrogatePK, Model):
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

    main_character_name = Column(db.Text, nullable=True)

    alt_application = Column(db.Boolean, default=False)

    characters = db.relationship('EveCharacter', secondary=character_apps,
                                 backref=db.backref('alt_apps', lazy='dynamic'))

    thesis = Column(db.Text, nullable=True)
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

    #reason_for_joining = Column(db.Text, nullable=True)
    find_out = Column(db.Text, nullable=True)

    favorite_role = Column(db.Text, nullable=True)

    last_update_time = Column(db.DateTime(), nullable=True)

    user_id = ReferenceCol('users', nullable=True)
    reviewer_user_id = ReferenceCol('users', nullable=True)
    last_user_id = ReferenceCol('users', nullable=True)

    approved_denied = Column(db.String(10), default="Pending")

    hidden = Column(db.Boolean, nullable=True, default=False)

    # search_vector = Column(TSVectorType('main_character_name', 'thesis'))

    user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
    reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
    last_action_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')


    # def __str__(self):
    #     return self.user.auth_info + " - Application"
    def __str__(self):
        return '<Application %r>' % self.user.auth_info



class HrApplicationComment(SurrogatePK, Model):
    __tablename__ = 'hr_comments'

    comment = Column(db.Text, nullable=True)

    application_id = ReferenceCol('hr_applications', nullable=False)
    user_id = ReferenceCol('users', nullable=False)

    last_update_time = Column(db.DateTime(), nullable=True)

    application = relationship('HrApplication', foreign_keys=[application_id], backref=db.backref('hr_comments', cascade="delete"), single_parent=True)

    user = relationship('User', backref=db.backref('hr_comments', lazy='dynamic'))

    def __repr__(self):
        return str(self.user) + " - Comment"




