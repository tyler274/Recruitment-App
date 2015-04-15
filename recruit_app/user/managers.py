# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter,\
    EveApiKeyPair, EveAllianceInfo, EveCorporationInfo, AuthInfo, User

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
            if unicode(api_key_pair.user_id) == unicode(user.id):
                if (dt.datetime.utcnow() - api_key_pair.last_update_time).total_seconds() >= 30:
                    # TODO: Switch from 30 second time out to the cache expiry time
                    EveManager.update_api_keypair(api_id=api_key_pair.api_id, api_key=api_key_pair.api_key)
                    return "Success"
                else:
                    return "Wait"
        else:
            return "Wrong User"

    @staticmethod
    def create_character(character_id, character_name, corporation_id, alliance_id, user_id, api_id):
        if not EveCharacter.query.filter_by(character_id=str(character_id)).first():
            eve_char = EveCharacter()
            eve_char.character_id = character_id
            eve_char.character_name = character_name
            eve_char.corporation_id = str(corporation_id)
            if alliance_id != 0:
                eve_char.alliance_id = str(alliance_id)
            eve_char.user_id = user_id
            eve_char.api_id = api_id
            if eve_char.save():
                return True
        return False


    @staticmethod
    def update_character(character_id, character_name, corporation_id, alliance_id, user_id, api_id):
        if EveCharacter.query.filter_by(character_id=str(character_id)).first():
            eve_char = EveCharacter.query.filter_by(character_id=str(character_id)).first()
            eve_char.character_id = str(character_id)
            eve_char.character_name = character_name
            eve_char.corporation_id = str(corporation_id)
            if alliance_id != 0:
                eve_char.alliance_id = str(alliance_id)

            eve_char.user_id = user_id
            eve_char.api_id = api_id
            if eve_char.save():
                return True
        return False


    @staticmethod
    def create_characters_from_list(chars, user, api_id):
        errors = []

        for char in chars.result:

            if not EveManager.check_if_character_exist(chars.result[char]['id']):
                if EveManager.create_character(chars.result[char]['id'],
                                            chars.result[char]['name'],
                                            chars.result[char]['corp']['id'],
                                            chars.result[char]['alliance']['id'],
                                            user.id, api_id):
                    pass

                else:
                    errors.append("Character Creation on " + chars.result[char]['name'] + " failed")

            else:
                if EveCharacter.query.filter_by(character_id=str(chars.result[char]['id'])).first().user_id is None:
                    if EveManager.update_character(chars.result[char]['id'],
                                                chars.result[char]['name'],
                                                chars.result[char]['corp']['id'],
                                                chars.result[char]['alliance']['id'],
                                                user.id, api_id):
                        pass

                    else:
                        errors.append("Character Creation/Update on " + chars.result[char]['name'] + " failed")
                else:
                        errors.append("Character " + chars.result[char]['name'] + " in use")
        return errors


    @staticmethod
    def create_corporations_from_character_list(characters):
        for character in characters.result:
            if not EveManager.check_if_corporation_exists_by_id(characters.result[character]['corp']['id']):
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
                if not EveManager.check_if_alliance_exists_by_id(characters.result[character]['alliance']['id']):
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
            if EveManager.check_if_character_exist(characters.result[character]['id']):
                eve_char = EveManager.get_character_by_character_name(characters.result[character]['name'])

                if str(characters.result[character]['alliance']['id']) != eve_char.alliance_id:

                    if characters.result[character]['alliance']['id'] != 0:
                        eve_char.alliance_id = str(characters.result[character]['alliance']['id'])

                    elif characters.result[character]['alliance']['id'] == 0:
                        eve_char.alliance_id = None

                if str(characters.result[character]['corp']['id']) != eve_char.corporation_id:
                    eve_char.corporation_id = str(characters.result[character]['corp']['id'])

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

            EveManager.update_characters_from_list(characters=characters,
                                                   user=api_pair.user,
                                                   api_id=api_pair.api_id)
            api_pair.last_update_time = dt.datetime.utcnow()
            api_pair.save()
            return True

        return False


    @staticmethod
    def create_alliance_info(alliance_id, alliance_name, alliance_ticker, alliance_executor_corp_id,
                             alliance_member_count, is_blue=None):
        if not EveManager.check_if_alliance_exists_by_id(str(alliance_id)):
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
        if EveManager.check_if_alliance_exists_by_id(alliance_id):
            alliance_info = EveAllianceInfo.query.filter_by(alliance_id=str(alliance_id)).all()
            alliance_info.executor_corp_id = str(alliance_executor_corp_id)
            alliance_info.member_count = alliance_member_count
            alliance_info.is_blue = is_blue
            alliance_info.save()

    @staticmethod
    def create_corporation_info(corporation_id, corp_name, corp_ticker, corp_member_count, alliance_id, is_blue=None):
        if not EveManager.check_if_corporation_exists_by_id(corporation_id):
            corp_info = EveCorporationInfo()
            corp_info.corporation_id = str(corporation_id)
            corp_info.corporation_name = corp_name
            corp_info.corporation_ticker = corp_ticker
            corp_info.member_count = corp_member_count
            corp_info.is_blue = is_blue
            if alliance_id:
                if alliance_id != 0:
                    corp_info.alliance_id = str(alliance_id)
            corp_info.save()

    @staticmethod
    def update_corporation_info(corporation_id, corp_member_count, alliance_id):
        corp_info = EveCorporationInfo.query.filter_by(corporation_id=str(corporation_id)).first()
        if corp_info:
            corp_info.member_count = corp_member_count
            if alliance_id:
                if alliance_id != 0:
                    corp_info.alliance_id = str(alliance_id)
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
            # Check that its owned by our user_id
            if unicode(api_key_pair.user_id) == unicode(user.id):
                api_key_pair.delete()

    @staticmethod
    def delete_characters_by_api_id_user(api_id, user):
        characters = EveCharacter.query.filter_by(api_id=api_id).all()
        if characters:
            # Check that its owned by our user_id

            for character in characters:
                if unicode(character.user.id) == unicode(user.id):
                    auth_info = AuthInfo.query.filter_by(main_character_id=character.character_id).first()
                    if auth_info:
                        auth_info.main_character_id = None
                        auth_info.save()

                    character.user_id = None
                    character.save()


    @staticmethod
    def delete_characters_by_api_id(api_id):
        characters = EveCharacter.query.filter_by(api_id=api_id).all()
        if characters:
            # Check that its owned by our user_id
            for character in characters:
                auth_info = AuthInfo.query.filter_by(main_character_id=character.character_id).first()
                if auth_info:
                    auth_info.main_character_id = None
                    auth_info.save()

                character.user_id = None
                character.save()


    @staticmethod
    def check_if_character_exist(character_id):
        if EveCharacter.query.filter_by(character_id=str(character_id)).first():
            return True
        return False


    @staticmethod
    def get_characters_by_owner(user):
        return EveCharacter.query.filter_by(user_id=user.id).all()

    @staticmethod
    def get_character_by_character_name(character_name):
        if EveCharacter.query.filter_by(character_name=character_name).first():
            return EveCharacter.query.filter_by(character_name=character_name).first()
        return None

    @staticmethod
    def get_character_by_id(character_id):
        if EveCharacter.query.filter_by(character_id=character_id).first():
            return EveCharacter.query.filter_by(character_id=character_id).first()
        return None

    @staticmethod
    def get_character_alliance_id_by_character_id(char_id):
        if EveCharacter.query.filter_by(character_id=char_id).all():
            return EveCharacter.query.filter_by(character_id=char_id).first().alliance_id

    @staticmethod
    def check_if_character_owned_by_user(character_id, user_id):
        character = EveCharacter.query.filter_by(character_id=str(character_id)).first()
        # print character
        if character:
            if str(character.user_id) == str(user_id):
                return True

        return False

    @staticmethod
    def check_if_alliance_exists_by_id(alliance_id):
        return EveAllianceInfo.query.filter_by(alliance_id=str(alliance_id)).all()

    @staticmethod
    def check_if_corporation_exists_by_id(corporation_id):
        if EveCorporationInfo.query.filter_by(corporation_id=str(corporation_id)).first():
            return True
        return False

    @staticmethod
    def get_alliance_info_by_id(alliance_id):
        if EveManager.check_if_alliance_exists_by_id(alliance_id):
            return EveAllianceInfo.query.filter_by(alliance_id=str(alliance_id)).first()
        else:
            return None

    @staticmethod
    def get_corporation_info_by_id(corp_id):
        if EveManager.check_if_corporation_exists_by_id(corp_id):
            return EveCorporationInfo.query.filter_by(corporation_id=corp_id).all()
        else:
            return None

    @staticmethod
    def get_all_corporation_info():
        return EveCorporationInfo.query.order_by(EveCorporationInfo.corporation_id)

    @staticmethod
    def get_all_alliance_info():
        return EveAllianceInfo.query.order_by(EveAllianceInfo.alliance_id)

class AuthInfoManager:
    def __init__(self):
        pass

    @staticmethod
    def get_or_create(user):
        auth_info = AuthInfo.query.filter_by(user_id=user.id).first()
        if auth_info:
            return auth_info
        else:
            # We have to create
            auth_info = AuthInfo()
            auth_info.user_id = user.id
            auth_info.save()
            return auth_info

    @staticmethod
    def update_main_character_id(char_id, user):
        auth_info = AuthInfoManager.get_or_create(user)
        auth_info.main_character_id = char_id
        auth_info.save()

    @staticmethod
    def create_role_pair(role_name):
        pass

    @staticmethod
    def check_if_role_leader(user):
        pass
