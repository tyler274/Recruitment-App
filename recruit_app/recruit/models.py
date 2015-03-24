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
    __searchable__ = ['about','user']

    main_character_id = ReferenceCol('characters', pk_name='character_id', nullable=True)
    main_character = relationship('EveCharacter', backref='applications')

    about = Column(db.Text)
    hours = Column(db.Integer)
    reason_for_joining = Column(db.Text)
    favorite_ship = Column(db.Text)
    favorite_role = Column(db.Text)
    most_fun = Column(db.Text)


    user_id = ReferenceCol('users', nullable=True)
    reviewer_user_id = ReferenceCol('users', nullable=True)
    last_user_id = ReferenceCol('users', nullable=True)

    approved_denied = db.Column(db.Boolean)

    user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
    reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
    last_action_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')


    # def __str__(self):
    #     return self.user.auth_info + " - Application"
    def __repr__(self):
        return '<Application %r>' % (self.user.auth_info)





