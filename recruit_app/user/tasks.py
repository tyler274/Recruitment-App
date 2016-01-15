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
        if EveApiManager.check_if_api_server_online():
            corporations = EveCorporationInfo.query.all()
            for corp in corporations:
                corp_info = EveApiManager.get_corporation_information(corp.corporation_id)
                if corp_info:
                    EveManager.update_corporation_info(corporation_id=corp_info['id'],
                        corp_member_count=corp_info['members']['current'],
                        alliance_id=corp_info['alliance']['id'])
                if corp.alliance_id:
                    alliance_info = EveApiManager.get_alliance_information(corp.alliance_id)
                    if alliance_info:
                        if not EveAllianceInfo.query.filter_by(alliance_id=corp.alliance_id).first():
                            EveManager.create_alliance_info(alliance_id=alliance_info['id'],
                                alliance_name=alliance_info['name'],
                                alliance_ticker=alliance_info['ticker'],
                                alliance_executor_corp_id=alliance_info['executor_id'],
                                alliance_member_count=alliance_info['member_count'])
                        else:
                            EveManager.update_alliance_info(alliance_id=alliance_info['id'],
                                alliance_executor_corp_id=alliance_info['executor_id'],
                                alliance_member_count=alliance_info['member_count'])


@job('low')
def run_api_key_update():
    with current_app.app_context():
        # I am not proud of this block of code
        if EveApiManager.check_if_api_server_online():
            api_keys = EveApiKeyPair.query.order_by(EveApiKeyPair.api_id).all()
            for api_key in api_keys:
                if EveApiManager.check_api_is_not_expire(api_key.api_id, api_key.api_key):
                    EveManager.update_api_keypair(
                        api_key.api_id, api_key.api_key)
                    current_app.logger.debug("Updating {0}".format(api_key.api_id))
                else:
                    current_app.logger.debug("Removing expired api_key {0} {1}".format(api_key.api_id, api_key.api_key))
                    EveManager.delete_api_key_pair(api_key.api_id, None)
