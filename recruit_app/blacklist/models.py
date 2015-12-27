# -*- coding: utf-8 -*-

from recruit_app.database import Column, db, Model, ReferenceCol, relationship, SurrogatePK, TimeMixin
from flask import current_app
import requests
import datetime as dt

class BlacklistCharacter(SurrogatePK, TimeMixin, Model):
    __tablename__ = 'blacklist_character'
    # __searchable__ = ['name', 'main_name', 'corporation', 'alliance', 'notes', 'ip_address']

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


# A cache table and wrapper for the GSF blacklist
class BlacklistGSF(TimeMixin, Model):
    __tablename__ = 'blacklist_gsf'
    
    status = Column(db.Unicode)
    character_id = ReferenceCol('characters', pk_name='character_id', primary_key=True)
    character = relationship('EveCharacter', foreign_keys=[character_id], backref='blacklist_gsf', cascade="delete")
    
    @staticmethod
    def getStatus(character):
        try:
            entry = BlacklistGSF.query.filter_by(character_id=character.character_id).one()
        except:
            # No entry, create a new one
            entry = BlacklistGSF()
            entry.character_id = character.character_id
            entry.status = u'UNKNOWN'
        
        if entry.last_update_time is None or (dt.datetime.utcnow() - entry.last_update_time).total_seconds() > 86400: # 1 day cache
            try:
                url = current_app.config['GSF_BLACKLIST_URL'] + character.character_name
                r   = requests.post(url)
                entry.status = str(r.json()[0]['output'])
                entry.last_update_time = dt.datetime.utcnow()
            except: # Will except on NONE for URL or connection issues.  Just keep status as UNKNOWN
                pass
            
            try:
                entry.save()
            except:
                # It's possible that multiple people are viewing the same new app at the same time, causing multiple threads to make the same cache object,
                # which throws an IntegrityError.  In that case just ignore the error, this is just a cache anyway.
                pass

        return entry.status

    def __repr__(self):
        return '<BlacklistCacheEntry' + ': ' + self.character_id + '>'
