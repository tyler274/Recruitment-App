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

class HrApplication(SurrogatePK, Model):
    __tablename__ = 'hr_applications'

    about = Column(db.Text)
    extra = Column(db.Text)
    scale = Column(db.Integer)
    reason_for_joining = Column(db.Text)



    user_id = ReferenceCol('users', nullable=True)
    reviewer_user_id = ReferenceCol('users', nullable=True)
    last_user_id = ReferenceCol('users', nullable=True)

    approved_denied = db.Column(db.Boolean)

    user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
    reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
    last_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')

    def __str__(self):
        return self.user.auth_info + " - Application"





