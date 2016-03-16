import evelink.api
import evelink.char
import evelink.eve
from flask import current_app
from recruit_app.extensions import cache_extension

class EveApiManager():

    def __init__(self):
        pass

    @staticmethod
    def evelink_api(**kwargs):
        return evelink.api.API(base_url=current_app.config['EVEAPI_URL'], **kwargs)

    @staticmethod
    def get_characters_from_api(api_id, api_key):
        chars = []
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            # Should get characters
            account = evelink.account.Account(api=api)
            chars = account.characters()
        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return chars

    @staticmethod
    def get_corporation_ticker_from_id(corp_id):
        ticker = ""
        try:
            api = EveApiManager.evelink_api()
            corp = evelink.corp.Corp(api)
            response = corp.corporation_sheet(corp_id)
            ticker = response[0]['ticker']
        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return ticker

    @staticmethod
    def get_alliance_information(alliance_id):
        results = {}
        try:
            alliances = EveApiManager.get_alliance_info()
            results = alliances[0][int(alliance_id)]
        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return results

    @staticmethod
    @cache_extension.cached(timeout=3600, key_prefix='get_alliance_info')
    def get_alliance_info():
        alliances = {}
        try:
            api = EveApiManager.evelink_api()
            eve = evelink.eve.EVE(api=api)
            alliances = eve.alliances()
        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return alliances


    @staticmethod
    def get_corporation_information(corp_id):
        results = {}
        try:
            api = EveApiManager.evelink_api()
            corp = evelink.corp.Corp(api=api)
            corpinfo = corp.corporation_sheet(corp_id=int(corp_id))
            results = corpinfo[0]
        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return results

    @staticmethod
    def check_api_is_type_account(api_id, api_key):
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            account = evelink.account.Account(api=api)
            info = account.key_info()
            return info[0]['type'] == "account"

        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return False

    @staticmethod
    def check_api_is_full(api_id, api_key):
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            account = evelink.account.Account(api=api)
            info = account.key_info()
            return info[0]['access_mask'] == current_app.config['API_MASK']

        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return False

    @staticmethod
    def check_api_is_not_expire(api_id, api_key):
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            account = evelink.account.Account(api=api)
            info = account.key_info()
            return info[0]['expire_ts'] is None

        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return False

    @staticmethod
    def get_api_info(api_id, api_key):
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            account = evelink.account.Account(api=api)
            info = account.key_info()
            return info

        except evelink.api.APIError as error:
            current_app.logger.error(error)

        return False

    @staticmethod
    def api_key_is_valid(api_id, api_key):
        try:
            api = EveApiManager.evelink_api(api_key=(api_id, api_key))
            account = evelink.account.Account(api=api)
            info = account.key_info()
            return True
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False

    @staticmethod
    def check_if_api_server_online():
        try:
            api = EveApiManager.evelink_api()
            server = evelink.server.Server(api=api)
            info = server.server_status()
            return True
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False

    @staticmethod
    def check_if_id_is_corp(corp_id):
        try:
            api = EveApiManager.evelink_api()
            corp = evelink.corp.Corp(api=api)
            corpinfo = corp.corporation_sheet(corp_id=int(corp_id))
            results = corpinfo[0]
            return True
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False

    @staticmethod
    def check_if_id_is_alliance(alliance_id):
        try:
            api = EveApiManager.evelink_api()
            eve = evelink.eve.EVE(api=api)
            alliance = eve.alliances()
            results = alliance[0][int(alliance_id)]
            if results:
                return True
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False

    @staticmethod
    def check_if_id_is_character(character_id):
        try:
            api = EveApiManager.evelink_api()
            eve = evelink.eve.EVE(api=api)
            results = eve.character_name_from_id(character_id)
            if results:
                return True
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False

    @staticmethod
    def check_if_character_is_in_corp(character_id, corp_id):
        try:
            api = EveApiManager.evelink_api()
            eve = evelink.eve.EVE(api=api)
            results = eve.affiliations_for_character(character_id)
            actual_corp = results[0]['corp']['id']
            return corp_id == actual_corp
        except evelink.api.APIError as error:
            current_app.logger.error(error)
            return False

        return False
