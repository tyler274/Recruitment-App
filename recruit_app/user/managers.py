# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter,\
    EveApiKeyPair, EveAllianceInfo, EveCorporationInfo, User

import datetime as dt

from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.extensions import bcrypt

from redis import Redis
redis_conn = Redis()

from rq.decorators import job

from flask import flash


class EveManager:
    def __init__(self):
        pass

    @staticmethod
    def update_user_api(api_id, user):
        api_key_pair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
        if api_key_pair:
            if unicode(api_key_pair.user_id) == unicode(user.id) or user.has_role('admin'):
                if (dt.datetime.utcnow() - api_key_pair.last_update_time).total_seconds() >= 30:
                    # TODO: Switch from 30 second time out to the cache expiry time
                    if EveManager.update_api_keypair(api_id=api_key_pair.api_id, api_key=api_key_pair.api_key):
                        return "Success"
                    else:
                        return "Failed"
                else:
                    return "Wait"
        else:
            return "Wrong User"

    @staticmethod
    def create_character(character_id, character_name, corporation_id, user_id, api_id):
        if not EveCharacter.query.filter_by(character_id=str(character_id)).first():
            eve_char = EveCharacter()
            eve_char.character_id = character_id
            eve_char.character_name = character_name
            eve_char.corporation_id = str(corporation_id)
            eve_char.user_id = user_id
            eve_char.api_id = api_id
            if eve_char.save():
                return True
        return False


    @staticmethod
    def update_character(character_id, character_name, corporation_id, user_id, api_id):
        eve_char = EveCharacter.query.filter_by(character_id=str(character_id)).first()
        if eve_char:
            eve_char.character_id = str(character_id)
            eve_char.character_name = character_name
            eve_char.corporation_id = str(corporation_id)
            eve_char.user_id = user_id
            eve_char.api_id = api_id
            
            for user in eve_char.previous_users:
                if user.id == int(user_id):
                    eve_char.previous_users.remove(user)
           
            if eve_char.save():
                return True
        return False


    @staticmethod
    def create_characters_from_list(chars, user, api_id):
        errors = []

        for char in chars.result:
            eveChar = EveManager.get_character_by_id(chars.result[char]['id'])
            if not eveChar:
                if EveManager.create_character(chars.result[char]['id'],
                                            chars.result[char]['name'],
                                            chars.result[char]['corp']['id'],
                                            user.id, api_id):
                    pass

                else:
                    errors.append("Character {0} creation failed".format(chars.result[char]['name']))

            else:
                if eveChar.user_id is None or not eveChar.api_id:
                    # Character exists, but isn't associated with a user or an api_key
                    if EveManager.update_character(chars.result[char]['id'],
                                                chars.result[char]['name'],
                                                chars.result[char]['corp']['id'],
                                                user.id, api_id):
                        pass

                    else:
                        errors.append("Character {0} update failed".format(chars.result[char]['name']))
                else:
                        errors.append("Character {0} in use by API {1}".format(chars.result[char]['name'], eveChar.api_id))
        return errors


    @staticmethod
    def create_corporations_from_character_list(characters):
        for character in characters.result:
            if not EveManager.get_corporation_info_by_id(characters.result[character]['corp']['id']):
                corp_info = EveApiManager.get_corporation_information(characters.result[character]['corp']['id'])
                if corp_info:
                    EveManager.create_corporation_info(corporation_id=corp_info['id'],
                                                       corp_name=corp_info['name'],
                                                       corp_ticker=corp_info['ticker'],
                                                       corp_member_count=corp_info['members']['current'],
                                                       alliance_id=corp_info['alliance']['id'])


    @staticmethod
    def create_alliances_from_list(characters):
        for character in characters.result:
            if characters.result[character]['alliance']['id'] != 0:
                if not EveManager.get_alliance_info_by_id(characters.result[character]['alliance']['id']):
                    alliance_info = EveApiManager.get_alliance_information(characters.result[character]['alliance']['id'])
                    # print alliance_info
                    if alliance_info:
                        EveManager.create_alliance_info(alliance_id=alliance_info['id'],
                                                        alliance_name=alliance_info['name'],
                                                        alliance_ticker=alliance_info['ticker'],
                                                        alliance_executor_corp_id=alliance_info['executor_id'],
                                                        alliance_member_count=alliance_info['member_count'])


    @staticmethod
    def update_characters_from_list(characters, user, api_id):
        EveManager.create_alliances_from_list(characters)
        EveManager.create_corporations_from_character_list(characters)
        EveManager.create_characters_from_list(characters, user, api_id)

        for character in characters.result:
            eve_char = EveManager.get_character_by_id(characters.result[character]['id'])
        
            if eve_char:
                if str(characters.result[character]['corp']['id']) != eve_char.corporation_id:
                    eve_char.corporation_id = str(characters.result[character]['corp']['id'])

                if str(characters.result[character]['alliance']['id']) != eve_char.corporation.alliance_id:
                    if characters.result[character]['alliance']['id'] != 0:
                        eve_char.corporation.alliance_id = str(characters.result[character]['alliance']['id'])
                    else:
                        eve_char.corporation.alliance_id = None
                    
                # Handle name changes (rare, but :CCP:)
                if characters.result[character]['name'] != eve_char.character_name:
                    eve_char.character_name = characters.result[character]['name']

                eve_char.save()


    @staticmethod
    def create_api_keypair(api_id, api_key, user_id):
        if not EveApiKeyPair.query.filter_by(api_id=api_id).all():
            api_pair = EveApiKeyPair()
            api_pair.api_id = api_id
            api_pair.api_key = api_key
            api_pair.last_update_time = dt.datetime.utcnow()
            api_pair.user_id = user_id
            api_pair.save()
            return True
        else:
            return False


    @staticmethod
    def update_api_keypair(api_id, api_key):
        # print "api update"
        api_pair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
        if api_pair:

            characters = EveApiManager.get_characters_from_api(api_id=api_id, api_key=api_key)
            if not characters:
                return False

            EveManager.update_characters_from_list(characters=characters,
                                                   user=api_pair.user,
                                                   api_id=api_pair.api_id)
                                                   
            # Now, archive any characters that don't exist anymore
            for old_api_char in api_pair.characters:
                found = False
                for char in characters.result:
                    if str(characters.result[char]['id']) == str(old_api_char.character_id):
                        found = True
                        break
                if not found:
                    for char in api_pair.user.previous_chars:
                        if str(old_api_char.character_id) == str(char.character_id):
                            found = True
                            break
                    if not found:
                        api_pair.user.previous_chars.append(old_api_char)
                    if str(api_pair.user.main_character_id) == str(old_api_char.character_id):
                        api_pair.user.main_character_id = None
                    api_pair.user.save(commit=False)
                    old_api_char.user_id = None
                    old_api_char.api_id = None
                    old_api_char.save(commit=False)                
            
            api_pair.last_update_time = dt.datetime.utcnow()
            api_pair.save()
            return True

        return False


    @staticmethod
    def create_alliance_info(alliance_id, alliance_name, alliance_ticker, alliance_executor_corp_id,
                             alliance_member_count, is_blue=None):
        if not EveManager.get_alliance_info_by_id(str(alliance_id)):
            alliance_info = EveAllianceInfo()
            alliance_info.alliance_id = str(alliance_id)
            alliance_info.alliance_name = alliance_name
            alliance_info.alliance_ticker = alliance_ticker
            alliance_info.executor_corp_id = str(alliance_executor_corp_id)
            alliance_info.member_count = alliance_member_count
            alliance_info.is_blue = is_blue
            alliance_info.save()

    @staticmethod
    def update_alliance_info(alliance_id, alliance_executor_corp_id, alliance_member_count, is_blue=None):
        alliance = EveManager.get_alliance_info_by_id(str(alliance_id))
        if alliance:
            alliance.executor_corp_id = str(alliance_executor_corp_id)
            alliance.member_count = alliance_member_count
            alliance.is_blue = is_blue
            alliance.save()

    @staticmethod
    def create_corporation_info(corporation_id, corp_name, corp_ticker, corp_member_count, alliance_id, is_blue=None):
        if not EveManager.get_corporation_info_by_id(corporation_id):
            corp_info = EveCorporationInfo()
            corp_info.corporation_id = str(corporation_id)
            corp_info.corporation_name = corp_name
            corp_info.corporation_ticker = corp_ticker
            corp_info.member_count = corp_member_count
            corp_info.is_blue = is_blue
            corp_info.alliance_id = alliance_id
            corp_info.save()

    @staticmethod
    def update_corporation_info(corporation_id, corp_member_count, alliance_id):
        corp_info = EveManager.get_corporation_info_by_id(str(corporation_id))
        if corp_info:
            corp_info.member_count = corp_member_count
            corp_info.alliance_id = alliance_id
            corp_info.save()

    @staticmethod
    def get_api_key_pairs(user):
        return EveApiKeyPair.query.filter_by(user_id=user.id).all()

    @staticmethod
    def check_if_api_key_pair_exist(api_id):
        if EveApiKeyPair.query.filter_by(api_id=api_id).first():
            return True
        else:
            return False

    @staticmethod
    def delete_api_key_pair(api_id, user):
        api_key_pair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
        if api_key_pair:
            # Lookup user if needed
            if not user:
                user = User.query.filter_by(id=api_key_pair.user_id).first()
                
            # Check that its owned by our user_id
            if user and unicode(api_key_pair.user_id) == unicode(user.id):
                # Unassociate any characters, but keep a history
                for char in api_key_pair.characters:
                    char.user_id = None
                    
                    # Don't add a duplicate entry to the history table.  Should never happen, but if someone has some messed up APIs or there's an odd char sell situation, it could be possible.
                    found = False
                    for prev_user in char.previous_users:
                        if prev_user.id == user.id:
                            found = True
                            break
                    if not found:
                        char.previous_users.append(user)
                    
                    if str(char.character_id) == str(user.main_character_id):
                        user.main_character_id = None
                        user.save()
                    
                    char.save()
                
                api_key_pair.delete()


    @staticmethod
    def get_characters_by_owner(user):
        return EveCharacter.query.filter_by(user_id=user.id).all()

    @staticmethod
    def get_character_by_id(character_id):
        return EveCharacter.query.filter_by(character_id=str(character_id)).first()

    @staticmethod
    def get_character_alliance_id_by_character_id(char_id):
        if EveCharacter.query.filter_by(character_id=str(char_id)).all():
            return EveCharacter.query.filter_by(character_id=str(char_id)).first().corporation.alliance_id

    @staticmethod
    def check_if_character_owned_by_user(character_id, user_id):
        character = EveCharacter.query.filter_by(character_id=str(character_id)).first()
        # print character
        if character:
            if str(character.user_id) == str(user_id):
                return True

        return False

    @staticmethod
    def get_alliance_info_by_id(alliance_id):
        return EveAllianceInfo.query.filter_by(alliance_id=str(alliance_id)).first()

    @staticmethod
    def get_corporation_info_by_id(corp_id):
        return EveCorporationInfo.query.filter_by(corporation_id=str(corp_id)).first()

    @staticmethod
    def get_all_corporation_info():
        return EveCorporationInfo.query.order_by(EveCorporationInfo.corporation_id)

    @staticmethod
    def get_all_alliance_info():
        return EveAllianceInfo.query.order_by(EveAllianceInfo.alliance_id)
