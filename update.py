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
        from recruit_app.user.tasks import run_alliance_corp_update, run_api_key_update
        

        from flask import current_app

        # run_alliance_corp_update()
        run_api_key_update()
