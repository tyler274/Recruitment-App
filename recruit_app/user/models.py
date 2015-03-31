# -*- coding: utf-8 -*-
import datetime as dt

#from flask_login import UserMixin
from flask_security import UserMixin, RoleMixin

from flask_security.utils import verify_and_update_password

from recruit_app.extensions import bcrypt
from recruit_app.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Role(SurrogatePK, Model, RoleMixin):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    #user_id = ReferenceCol('users', nullable=True)
    #user = relationship('User', backref='roles')

    # def __init__(self, name, **kwargs):
    #     db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class RolePair(SurrogatePK, Model):
    __tablename__ = 'role_pair'
    member_role_id = ReferenceCol('roles', nullable=True)
    leader_role_id = ReferenceCol('roles', nullable=True)
    name = Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    member_role = relationship('Role', foreign_keys=[member_role_id], backref='member_pairs')
    reviewer_user = relationship('Role', foreign_keys=[leader_role_id], backref='leader_pairs')

    def __repr__(self):
        return '<RolePair({name})>'.format(name=self.name)


class User(SurrogatePK, Model, UserMixin):
    __tablename__ = 'users'

    username = Column(db.String(80), unique=True, nullable=True)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    confirmed_at = Column(db.DateTime, nullable=True)

    last_login_at = Column(db.DateTime())
    current_login_at = Column(db.DateTime())
    last_login_ip = Column(db.String(100))
    current_login_ip = Column(db.String(100))
    login_count = Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # def __init__(self, username, email, password=None, **kwargs):
    #     db.Model.__init__(self, username=username, email=email, **kwargs)
    #     if password:
    #         self.set_password(password)
    #     else:
    #         self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    # def __repr__(self):
    #     return '<User({username!r})>'.format(username=self.username)
    def __repr__(self):
        return '<User({name})>'.format(name=self.email)



class AuthInfo(SurrogatePK, Model):
    __tablename__ = 'auth_info'

    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='auth_info')

    main_character_id = ReferenceCol('characters', pk_name='character_id', nullable=True)
    main_character = relationship('EveCharacter', lazy='subquery', backref=db.backref('auth_info', lazy='dynamic'))

    def __repr__(self):
        return '<AuthInfo({name})>'.format(name=self.user)


class EveCharacter(Model):
    __tablename__ = 'characters'

    character_id = Column(db.String(254), unique=True, primary_key=True)
    character_name = Column(db.String(254))
    corporation_id = ReferenceCol('corporations', pk_name='corporation_id', nullable=True)
    corporation = relationship('EveCorporationInfo', backref='characters')

    alliance_id = ReferenceCol('alliances', pk_name='alliance_id', nullable=True)
    alliance = relationship('EveAllianceInfo', backref='characters')

    api_id = ReferenceCol('api_key_pairs', pk_name='api_id', nullable=True)
    api = relationship('EveApiKeyPair', backref='characters')

    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='characters')

    skillpoints = Column(db.Integer, nullable=True)

    # def __init__(self, character_id, character_name, corporation_id,  **kwargs):
    #     db.Model.__init__(self, character_id=character_id, character_name=character_name, corporation_id=corporation_id, **kwargs)

    #hr_applications = db.relationship('HrApplications', backref='person', lazy='dynamic')
    #hr_comments = db.relationship('Comments', backref='person', lazy='dynamic')

    def __str__(self):
        return self.character_name


class EveApiKeyPair(Model):
    __tablename__ = 'api_key_pairs'

    api_id = Column(db.String(254), unique=True, primary_key=True)
    api_key = Column(db.String(254))
    last_update_time = Column(db.DateTime(), nullable=True)

    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='api_keys')

    # def __init__(self, api_id, api_key, user_id,  **kwargs):
    #     db.Model.__init__(self, api_id=api_id, api_key=api_key, user_id=user_id, **kwargs)

    def __str__(self):
        return self.api_id

class EveAllianceInfo(Model):
    __tablename__ = 'alliances'

    alliance_id = Column(db.String(254), unique=True, primary_key=True)
    alliance_name = Column(db.String(254))
    alliance_ticker = Column(db.String(254))
    executor_corp_id = Column(db.String(254))
    is_blue = Column(db.Boolean, default=False)
    member_count = Column(db.Integer)

    # def __init__(self, alliance_id, alliance_name, alliance_ticker, executor_corp_id,  **kwargs):
    #     db.Model.__init__(self, alliance_id=alliance_id, alliance_name=alliance_name, alliance_ticker=alliance_ticker, **kwargs)

    def __str__(self):
        return self.alliance_name


class EveCorporationInfo(Model):
    __tablename__ = 'corporations'

    corporation_id = Column(db.String(254), unique=True, primary_key=True)
    corporation_name = Column(db.String(254))
    corporation_ticker = Column(db.String(254))
    member_count = Column(db.Integer)
    is_blue = Column(db.Boolean, default=False)
    alliance_id = ReferenceCol('alliances', pk_name='alliance_id', nullable=True)
    alliance = relationship('EveAllianceInfo', backref='corporations')

    # def __init__(self, corporation_id, corporation_name, corporation_ticker, member_count=member_count,  **kwargs):
    #     db.Model.__init__(self, corporation_id=corporation_id, corporation_name=corporation_name, corporation_ticker=corporation_ticker, **kwargs)

    def __str__(self):
        return self.corporation_name

# class HrApplication(SurrogatePK, Model):
#     __tablename__ = 'hr_applications'

#     main_character_id = ReferenceCol('characters', pk_name='character_id', nullable=True)
#     main_character = relationship('EveCharacter', backref='auth_info')
#     about = Column(db.Text)
#     extra = Column(db.Text)

#     user_id = ReferenceCol('users', nullable=True)
#     reviewer_user_id = ReferenceCol('users', nullable=True)
#     last_user_id = ReferenceCol('users', nullable=True)

#     approved_denied = db.Column(db.Boolean)

#     user = relationship('User', foreign_keys=[user_id], backref='hr_applications')
#     reviewer_user = relationship('User', foreign_keys=[reviewer_user_id], backref='hr_applications_reviewed')
#     last_user = relationship('User', foreign_keys=[last_user_id], backref='hr_applications_touched')

#     def __str__(self):
#         return self.character_name + " - Application"


# class HrApplicationComment(SurrogatePK, Model):
#     __tablename__ = 'hr_application_comments'

#     comment = Column(db.Text)

#     application_id = ReferenceCol('hr_applications', nullable=False)
#     application = relationship('HrApplication', backref='comments')

#     user_id = ReferenceCol('users', nullable=True)
#     user = relationship('User', backref='hr_application_comments')
