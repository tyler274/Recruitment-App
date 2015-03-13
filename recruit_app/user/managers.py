# -*- coding: utf-8 -*-
from models import EveCharacter
from models import EveApiKeyPair
from models import EveAllianceInfo
from models import EveCorporationInfo
from models import AuthInfo
from models import User

import datetime as dt

from .eve_api_manager import EveApiManager


class EveManager:
    def __init__(self):
        pass

    @staticmethod
    def create_character(character_id, character_name, corporation_id,
                         corporation_name, corporation_ticker, alliance_id,
                         alliance_name, user_id, api_id):

        if not EveCharacter.query.filter_by(character_id=character_id).all():
            eve_char = EveCharacter()
            eve_char.character_id = character_id
            eve_char.character_name = character_name
            eve_char.corporation_id = corporation_id
            eve_char.corporation_name = corporation_name
            eve_char.corporation_ticker = corporation_ticker
            eve_char.alliance_id = alliance_id
            eve_char.alliance_name = alliance_name
            eve_char.user_id = user_id
            eve_char.api_id = api_id
            eve_char.save()

    @staticmethod
    def create_characters_from_list(chars, user_id, api_id):
        for char in chars.result:
            if not EveManager.check_if_character_exist(chars.result[char]['name']):
                EveManager.create_character(chars.result[char]['id'],
                                            chars.result[char]['name'],
                                            chars.result[char]['corp']['id'],
                                            chars.result[char]['corp']['name'],
                                            EveApiManager.get_corporation_ticker_from_id(
                                                chars.result[char]['corp']['id']),
                                            chars.result[char]['alliance']['id'],
                                            chars.result[char]['alliance']['name'],
                                            user_id, api_id)

    @staticmethod
    def update_characters_from_list(characters):
        for character in characters:
            if EveManager.check_if_character_exist(chars.result[char]['name']):
                eve_char = EveManager.get_character_by_character_name(chars.result[char]['name'])
                eve_char.corporation_id = chars.result[char]['corp']['id']
                eve_char.alliance_id = chars.result[char]['alliance']['id']
                eve_char.save()


    @staticmethod
    def create_api_keypair(api_id, api_key, user_id):
        if not EveApiKeyPair.query.filter_by(api_id=api_id).all():
            api_pair = EveApiKeyPair()
            api_pair.api_id = api_id
            api_pair.api_key = api_key
            api_pair.update_time = dt.datetime.now()
            api_pair.user_id = user_id
            api_pair.save()


    @staticmethod
    def update_api_keypair(api_id, api_key):
        if EveApiKeyPair.query.filter_by(api_id=api_id).first():
            api_pair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
            characters = EveApiManager.get_characters_from_api(api_id=api_id, api_key=api_key)
            update_characters_from_list(characters=characters)
            api_pair.update_time = dt.datetime.now()
            api_pair.save()


    @staticmethod
    def create_alliance_info(alliance_id, alliance_name, alliance_ticker, alliance_executor_corp_id,
                             alliance_member_count, is_blue=None):
        if not EveManager.check_if_alliance_exists_by_id(alliance_id):
            alliance_info = EveAllianceInfo()
            alliance_info.alliance_id = alliance_id
            alliance_info.alliance_name = alliance_name
            alliance_info.alliance_ticker = alliance_ticker
            alliance_info.executor_corp_id = alliance_executor_corp_id
            alliance_info.member_count = alliance_member_count
            alliance_info.is_blue = is_blue
            alliance_info.save()

    @staticmethod
    def update_alliance_info(alliance_id, alliance_executor_corp_id, alliance_member_count, is_blue=None):
        if EveManager.check_if_alliance_exists_by_id(alliance_id):
            alliance_info = EveAllianceInfo.query.filter_by(alliance_id=alliance_id).all()
            alliance_info.executor_corp_id = alliance_executor_corp_id
            alliance_info.member_count = alliance_member_count
            alliance_info.is_blue = is_blue
            alliance_info.save()

    @staticmethod
    def create_corporation_info(corp_id, corp_name, corp_ticker, corp_member_count, alliance_id, is_blue=None):
        if not EveManager.check_if_corporation_exists_by_id(corp_id):
            corp_info = EveCorporationInfo()
            corp_info.corporation_id = corp_id
            corp_info.corporation_name = corp_name
            corp_info.corporation_ticker = corp_ticker
            corp_info.member_count = corp_member_count
            corp_info.is_blue = is_blue
            if alliance_id:
                corp_info.alliance_id = alliance_id
            corp_info.save()

    @staticmethod
    def update_corporation_info(corp_id, corp_member_count, alliance_id, is_blue):
        if EveManager.check_if_corporation_exists_by_id(corp_id):
            corp_info = EveCorporationInfo.query.filter_by(corporation_id=corp_id).all()
            corp_info.member_count = corp_member_count
            corp_info.alliance_id = alliance_id
            corp_info.is_blue = is_blue
            corp_info.save()

    @staticmethod
    def get_api_key_pairs(user_id):
        if EveApiKeyPair.query.filter_by(user_id=user_id).all():
            return EveApiKeyPair.query.filter_by(user_id=user_id).all()

    @staticmethod
    def check_if_api_key_pair_exist(api_id):
        if EveApiKeyPair.query.filter_by(api_id=api_id).first():
            return True
        else:
            return False

    @staticmethod
    def delete_api_key_pair(api_id, user_id):
        if EveApiKeyPair.query.filter_by(api_id=api_id).all():
            # Check that its owned by our user_id
            apikeypair = EveApiKeyPair.query.filter_by(api_id=api_id).first()
            if unicode(apikeypair.user_id) == unicode(user_id):
                apikeypair.delete()

    @staticmethod
    def delete_characters_by_api_id(api_id, user_id):
        if EveCharacter.query.filter_by(api_id=api_id).all():
            # Check that its owned by our user_id
            characters = EveCharacter.query.filter_by(api_id=api_id).all()

            for character in characters:
                if unicode(character.user_id) == unicode(user_id):
                    character.delete()


    @staticmethod
    def check_if_character_exist(character_id):
        if EveCharacter.query.filter_by(character_name=character_name).first():
            return True
        return False


    @staticmethod
    def get_characters_by_owner_id(user_id):
        if EveCharacter.query.filter_by(user_id=user_id).all():
            return EveCharacter.query.filter_by(user_id=user_id).all()
        return None

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
    def get_character_alliance_id_by_id(char_id):
        if EveCharacter.query.filter_by(character_id=char_id).all():
            return EveCharacter.query.filter_by(character_id=char_id).first().alliance_id

    @staticmethod
    def check_if_character_owned_by_user(character_id, user_id):
        character = EveCharacter.query.filter_by(character_id=character_id).first()
        print character
        if unicode(character.user_id) == unicode(user_id):
            return True

        return False

    @staticmethod
    def check_if_alliance_exists_by_id(alliance_id):
        return EveAllianceInfo.query.filter_by(alliance_id=alliance_id).all()

    @staticmethod
    def check_if_corporation_exists_by_id(corporation_id):
        if EveCorporationInfo.query.filter_by(corporation_id=corporation_id).first():
            return True
        return False

    @staticmethod
    def get_alliance_info_by_id(alliance_id):
        if EveManager.check_if_alliance_exists_by_id(alliance_id):
            return EveAllianceInfo.query.filter_by(alliance_id=alliance_id).first()
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
    def get_or_create(user_id):
        if AuthInfo.query.filter_by(user_id=user_id).all():
            return AuthInfo.query.filter_by(user_id=user_id).first()
        else:
            # We have to create
            authinfo = AuthInfo()
            authinfo.user_id = user_id
            authinfo.save()
            return authinfo

    @staticmethod
    def update_main_character_id(char_id, user_id):
        if User.query.filter_by(id=user_id).all():
            authinfo = AuthInfoManager.get_or_create(user_id)
            authinfo.main_character_id = char_id
            authinfo.save()
