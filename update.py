import os, sys
from recruit_app.app import create_app
from recruit_app.settings import DevConfig, ProdConfig

if __name__ == '__main__':
    if os.environ.get("RECRUIT_APP_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)
        
    with app.app_context():
        from recruit_app.user.tasks import run_alliance_corp_update, run_api_key_update
        
        if len(sys.argv) < 2:
            print 'Please specific corp, api_key, or all.'
            sys.exit()
        if sys.argv[1] == 'corp' or sys.argv[1] == 'all':
            run_alliance_corp_update()
        if sys.argv[1] == 'api_key' or sys.argv[1] == 'all':
            run_api_key_update()
