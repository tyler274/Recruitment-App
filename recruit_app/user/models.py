# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin

from recruit_app.extensions import bcrypt
from recruit_app.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)

class AuthInfo(SurrogatePK, Model):
    __tablename__ = 'auth_info'

    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='auth_info')

    main_character_id = ReferenceCol('characters', nullable=True)
    main_character = relationship('EveCharacter', backref='auth_info')


class EveCharacter(SurrogatePK, Model):
    __tablename__ = 'characters'

    character_id = Column(db.String(254))
    character_name = Column(db.String(254))
    corporation_id = ReferenceCol('corporations', nullable=True)
    corporation = relationship('EveCorporationInfo', backref='characters')

    alliance_id = ReferenceCol('alliances', nullable=True)
    alliance = relationship('EveAllianceInfo', backref='characters')

    api_id = ReferenceCol('api_key_pairs', nullable=True)
    api = relationship('EveApiKeyPair', backref='characters')

    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='characters')

    # def __init__(self, character_id, character_name, corporation_id,  **kwargs):
    #     db.Model.__init__(self, character_id=character_id, character_name=character_name, corporation_id=corporation_id, **kwargs)

    #hr_applications = db.relationship('HrApplications', backref='person', lazy='dynamic')
    #hr_comments = db.relationship('Comments', backref='person', lazy='dynamic')

    def __str__(self):
        return self.character_name


class EveApiKeyPair(SurrogatePK, Model):
    __tablename__ = 'api_key_pairs'

    api_id = Column(db.String(254))
    api_key = Column(db.String(254))
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='api_keys')

    # def __init__(self, api_id, api_key, user_id,  **kwargs):
    #     db.Model.__init__(self, api_id=api_id, api_key=api_key, user_id=user_id, **kwargs)

    def __str__(self):
        return self.user.username + " - ApiKeyPair"


class EveAllianceInfo(SurrogatePK, Model):
    __tablename__ = 'alliances'

    alliance_id = Column(db.String(254), unique=True)
    alliance_name = Column(db.String(254))
    alliance_ticker = Column(db.String(254))
    executor_corp_id = Column(db.String(254))
    is_blue = Column(db.Boolean, default=False)
    member_count = Column(db.Integer)

    # def __init__(self, alliance_id, alliance_name, alliance_ticker, executor_corp_id,  **kwargs):
    #     db.Model.__init__(self, alliance_id=alliance_id, alliance_name=alliance_name, alliance_ticker=alliance_ticker, **kwargs)

    def __str__(self):
        return self.alliance_name


class EveCorporationInfo(SurrogatePK, Model):
    __tablename__ = 'corporations'

    corporation_id = Column(db.String(254), unique=True)
    corporation_name = Column(db.String(254))
    corporation_ticker = Column(db.String(254))
    member_count = Column(db.Integer)
    is_blue = Column(db.Boolean, default=False)
    alliance_id = ReferenceCol('alliances', nullable=True)
    alliance = relationship('EveAllianceInfo', backref='corporations')

    # def __init__(self, corporation_id, corporation_name, corporation_ticker, member_count=member_count,  **kwargs):
    #     db.Model.__init__(self, corporation_id=corporation_id, corporation_name=corporation_name, corporation_ticker=corporation_ticker, **kwargs)

    def __str__(self):
        return self.corporation_name
