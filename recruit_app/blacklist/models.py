# -*- coding: utf-8 -*-

from recruit_app.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
    TimeMixin,
)

class BlacklistCharacter(SurrogatePK, TimeMixin, Model):
    __tablename__ = 'blacklist_character'
    __searchable__ = ['name', 'main_name', 'corporation', 'alliance', 'notes', 'ip_address']

    name = Column(db.Unicode, nullable=True)
    main_name = Column(db.Unicode, nullable=True)
    corporation = Column(db.Unicode)
    alliance = Column(db.Unicode)
    notes = Column(db.Unicode)

    ip_address = Column(db.Unicode)

    creator_id = ReferenceCol('users', nullable=True)
    creator = relationship('User', foreign_keys=[creator_id], backref='blacklist_character_entries')

    def __repr__(self):
        return '<' + self.name + ': ' + self.notes + '>'

    # @property
    # def creator_name(self):
    #     return self.creator.auth_info[0].main_character.character_name
