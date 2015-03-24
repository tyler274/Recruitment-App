from recruit_app.user.models import EveCharacter, EveCorporationInfo, EveAllianceInfo
from recruit_app.user.managers import EveManager
from recruit_app.user.eve_api_manager import EveApiManager



# Run Every 2 hours
# @periodic_task(run_every=crontab(minute=0, hour="*/2"))
def run_alliance_corp_update():
    # I am not proud of this block of code
    if EveApiManager.check_if_api_server_online():
        characters = EveCharacter.query.order_by(EveCharacter.character_id).all()
        for character in characters:
            if not EveCorporationInfo.query.filter_by(corporation_id=character.corporation_id).first():
                corpinfo = EveApiManager.get_corporation_information(character.corporation_id)
                if corpinfo:
                    # print corpinfo
                    EveManager.create_corporation_info(corp_id=corpinfo['id'], corp_name=corpinfo['name'], corp_ticker=corpinfo['ticker'], corp_member_count=corpinfo['members']['current'], alliance_id=corpinfo['alliance']['id'])
            if int(character.alliance_id) != 0:
                if not EveAllianceInfo.query.filter_by(alliance_id=character.alliance_id).first():
                    print character.alliance_id
                    allianceinfo = EveApiManager.get_alliance_information(character.alliance_id)
                    if allianceinfo:
                        # print allianceinfo
                        EveManager.create_alliance_info(alliance_id=allianceinfo['id'], alliance_name=allianceinfo['name'], alliance_ticker=allianceinfo['ticker'], alliance_executor_corp_id=allianceinfo['executor_id'], alliance_member_count=allianceinfo['member_count'])


