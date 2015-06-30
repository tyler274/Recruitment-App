# -*- coding: utf-8 -*-

from recruit_app.extensions import bcrypt
from recruit_app.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
    TimeMixin,
)

import flask_whooshalchemy as whooshalchemy
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType, ScalarListType

from sqlalchemy_searchable import SearchQueryMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy.dialects import postgresql


make_searchable()

class BlacklistCharacter(SurrogatePK, TimeMixin, Model):
    __tablename__ = 'blacklist_character'
    __searchable__ = ['name', 'main_name', 'corporation', 'alliance', 'notes']

    name = Column(db.Unicode, nullable=False)
    main_name = Column(db.Unicode, nullable=True)
    corporation = Column(db.Unicode)
    alliance = Column(db.Unicode)
    notes = Column(db.Unicode)

    creator_id = ReferenceCol('users', nullable=True)
    creator = relationship('User', foreign_keys=[creator_id], backref='blacklist_character_entries')
