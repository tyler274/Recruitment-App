# -*- coding: utf-8 -*-
from .models import BlacklistCharacter

class BlacklistManager:
    def __init__(self):
        pass

    @staticmethod
    def create_entry(entry_data, user):
        try:
            entry = BlacklistCharacter()
            entry.name = entry_data.character_name.data
            entry.main_name = entry_data.main_name.data
            entry.corporation = entry_data.corporation.data
            entry.alliance = entry_data.alliance.data
            entry.notes = entry_data.notes.data
            entry.creator = user
            entry.save()
            return True
        except:
            return False

