from recruit_app.user.models import EveCharacter, EveCorporationInfo, EveAllianceInfo, EveApiKeyPair
from recruit_app.user.managers import EveManager
from recruit_app.user.eve_api_manager import EveApiManager

from flask_rq import job, get_worker
from flask import current_app
from recruit_app.extensions import rq

from redis import Redis
import time

# Run Every 2 hours
# @periodic_task(run_every=crontab(minute=0, hour="*/2"))
@job('low')
def run_alliance_corp_update():
    with current_app.app_context():
        # I am not proud of this block of code
        if EveApiManager.check_if_api_server_online():
            characters = EveCharacter.query.order_by(EveCharacter.character_id).all()
            for character in characters:
                # print character
                corp_info = EveApiManager.get_corporation_information(character.corporation_id)
                if corp_info:
                    if not EveCorporationInfo.query.filter_by(corporation_id=character.corporation_id).first():
                        # print corp_info
                        # print "creating corp: " + corp_info
                        EveManager.create_corporation_info(corporation_id=corp_info['id'],
                                                           corp_name=corp_info['name'],
                                                           corp_ticker=corp_info['ticker'],
                                                           corp_member_count=corp_info['members']['current'],
                                                           alliance_id=corp_info['alliance']['id'])
                    else:
                        # print "updating corp: " + corp_info
                        EveManager.update_corporation_info(corporation_id=corp_info['id'],
                                                           corp_member_count=corp_info['members']['current'],
                                                           alliance_id=corp_info['alliance']['id'])
                if character.corporation.alliance_id:
                    if character.corporation.alliance_id != "0":
                        alliance_info = EveApiManager.get_alliance_information(character.corporation.alliance_id)
                        if alliance_info:
                            if not EveAllianceInfo.query.filter_by(alliance_id=character.corporation.alliance_id).first():
                                # print alliance_info
                                # print "creating alliance: " + alliance_info
                                EveManager.create_alliance_info(alliance_id=alliance_info['id'],
                                                                alliance_name=alliance_info['name'],
                                                                alliance_ticker=alliance_info['ticker'],
                                                                alliance_executor_corp_id=alliance_info['executor_id'],
                                                                alliance_member_count=alliance_info['member_count'])
                            else:
                                # print alliance_info
                                # print "updating alliance: " + alliance_info
                                EveManager.update_alliance_info(alliance_id=alliance_info['id'],
                                                                alliance_name=alliance_info['name'],
                                                                alliance_ticker=alliance_info['ticker'],
                                                                alliance_executor_corp_id=alliance_info['executor_id'],
                                                                alliance_member_count=alliance_info['member_count'])

@job('low')
def run_api_key_update():
    with current_app.app_context():
        # I am not proud of this block of code
        if EveApiManager.check_if_api_server_online():
            api_keys = EveApiKeyPair.query.order_by(EveApiKeyPair.api_id).all()
            for api_key in api_keys:
                good = True
                
                if not EveApiManager.check_api_is_type_account(api_key.api_id, api_key.api_key):
                    good = False
                    print "Removing invalid account API key {0} {1}\n".format(api_key.api_id, api_key.api_key)
                if not EveApiManager.check_api_is_full(api_key.api_id, api_key.api_key):
                    print "Warning API {0} {1} for user {2} is not full\n".format(api_key.api_id, api_key.api_key, api_key.user.email)
                if not EveApiManager.check_api_is_not_expire(api_key.api_id, api_key.api_key):
                    good = False
                    print "Removing expired api_key {0} {1}".format(api_key.api_id, api_key.api_key)
                    
                if good:
                    EveManager.update_api_keypair(api_key.api_id, api_key.api_key)
                else:
                    EveManager.delete_api_key_pair(api_key.api_id, None)
                # Max API check is 30req/s
                sleep(1.0/30.0)
