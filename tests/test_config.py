# -*- coding: utf-8 -*-
from recruit_app.app import create_app
from recruit_app.settings import ProdConfig, DevConfig

def test_production_config():
    pass
    #TODO Fix these later
    # app = create_app(ProdConfig)
    # assert app.config['ENV'] == 'prod'
    # assert app.config['DEBUG'] is False
    # assert app.config['DEBUG_TB_ENABLED'] is False
    # assert app.config['ASSETS_DEBUG'] is False


def test_dev_config():
    pass
    #TODO Fix these later
    # app = create_app(DevConfig)
    # assert app.config['ENV'] == 'dev'
    # assert app.config['DEBUG'] is True
    # assert app.config['ASSETS_DEBUG'] is True
