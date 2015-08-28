import os
from recruit_app.app import create_app
from recruit_app.settings import DevConfig, ProdConfig

if __name__ == '__main__':
    if os.environ.get("RECRUIT_APP_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)

    with app.app_context():
        from recruit_app.user.models import EveCharacter, EveCorporationInfo, EveAllianceInfo, EveApiKeyPair
        from recruit_app.user.managers import EveManager
        from recruit_app.user.eve_api_manager import EveApiManager

        from flask import current_app

        def run_alliance_corp_update():
            # I am not proud of this block of code
            if EveApiManager.check_if_api_server_online():
                characters = EveCharacter.query.order_by(EveCharacter.character_id).all()
                for character in characters:
                    print character
                    corp_info = EveApiManager.get_corporation_information(character.corporation_id)
                    if corp_info:
                        if not EveCorporationInfo.query.filter_by(corporation_id=character.corporation_id).first():
                            # print corp_info
                            #print "creating corp: " + corp_info
                            EveManager.create_corporation_info(corporation_id=corp_info['id'],
                                                               corp_name=corp_info['name'],
                                                               corp_ticker=corp_info['ticker'],
                                                               corp_member_count=corp_info['members']['current'],
                                                               alliance_id=corp_info['alliance']['id'])
                        else:
                            #print "updating corp: " + corp_info
                            EveManager.update_corporation_info(corporation_id=corp_info['id'],
                                                               corp_member_count=corp_info['members']['current'],
                                                               alliance_id=corp_info['alliance']['id'])
                    if character.alliance_id:
                        if character.alliance_id != "0":
                            alliance_info = EveApiManager.get_alliance_information(character.alliance_id)
                            if alliance_info:
                                if not EveAllianceInfo.query.filter_by(alliance_id=character.alliance_id).first():
                                    # print alliance_info
                                    #print "creating alliance: " + alliance_info
                                    EveManager.create_alliance_info(alliance_id=alliance_info['id'],
                                                                    alliance_name=alliance_info['name'],
                                                                    alliance_ticker=alliance_info['ticker'],
                                                                    alliance_executor_corp_id=alliance_info['executor_id'],
                                                                    alliance_member_count=alliance_info['member_count'])
                                else:
                                    # print alliance_info
                                    #print "updating alliance: " + alliance_info
                                    EveManager.create_alliance_info(alliance_id=alliance_info['id'],
                                                                    alliance_name=alliance_info['name'],
                                                                    alliance_ticker=alliance_info['ticker'],
                                                                    alliance_executor_corp_id=alliance_info['executor_id'],
                                                                    alliance_member_count=alliance_info['member_count'])

        def delete_characters_by_api(api_id):
            characters = EveCharacter.query.filter_by(api_id=api_id).all()
            for character in characters:
                character.user_id = None
                character.save()

        def run_api_key_update():
            # I am not proud of this block of code
            if EveApiManager.check_if_api_server_online():
                api_keys = EveApiKeyPair.query.order_by(EveApiKeyPair.api_id).all()
                for api_key in api_keys:
                    if not EveApiManager.check_api_is_type_account(api_key.api_id, api_key.api_key):
                        #print "removing characters from" + api_key
                        delete_characters_by_api(api_key.api_id)

                    if not EveApiManager.check_api_is_full(api_key.api_id, api_key.api_key):
                        #print "removing characters from" + api_key
                        delete_characters_by_api(api_key.api_id)

                    if not EveApiManager.check_api_is_not_expire(api_key.api_id, api_key.api_key):
                        #print "removing characters from" + api_key
                        delete_characters_by_api(api_key.api_id)

                    EveManager.update_api_keypair(api_key.api_id, api_key.api_key)

        # run_alliance_corp_update()
        run_api_key_update()
