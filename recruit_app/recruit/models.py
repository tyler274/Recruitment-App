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

class HrApplication(SurrogatePK, Model):
    __tablename__ = 'hr_applications'
    __searchable__ = ['about']

    #main_character_id = ReferenceCol('characters', pk_name='character_id', nullable=True)
    #main_character = relationship('EveCharacter', backref='applications')

    about = Column(db.Text, nullable=True)
    scale = Column(db.Integer, nullable=True)
    reason_for_joining = Column(db.Text, nullable=True)
    favorite_ship = Column(db.Text, nullable=True)
    favorite_role = Column(db.Text, nullable=True)
    most_fun = Column(db.Text, nullable=True)

    last_update_time = Column(db.DateTime(), nullable=True)

    user_id = ReferenceCol('users', nullable=True)
    reviewer_user_id = ReferenceCol('users', nullable=True)
    last_user_id = ReferenceCol('users', nullable=True)

    approved_denied = Column(db.String(10), default="Pending")

    user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
    reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
    last_action_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')


    # def __str__(self):
    #     return self.user.auth_info + " - Application"
    def __repr__(self):
        return '<Application %r>' % (self.user.auth_info)

class HrApplicationComment(SurrogatePK, Model):
    __tablename__ = 'hr_comments'

    comment = Column(db.Text, nullable=True)

    application_id = ReferenceCol('hr_applications', nullable=False)
    used_id = ReferenceCol('users', nullable=False)

    last_update_time = Column(db.DateTime(), nullable=True)

    application = relationship('HrApplication', cascade='all, delete-orphan', foreign_keys=[application_id], backref=db.backref('hr_comments', cascade="all,delete"), single_parent=True)

    user = relationship('User', backref=db.backref('hr_comments', lazy='dynamic'))

    def __repr__(self):
        return str(self.user.auth_info) + " - Comment"




