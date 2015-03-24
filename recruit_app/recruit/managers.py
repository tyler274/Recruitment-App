# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter, EveApiKeyPair, EveAllianceInfo, EveCorporationInfo, AuthInfo, User

from recruit_app.recruit.models import HrApplication

import datetime as dt

from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.extensions import bcrypt

from redis import Redis
redis_conn = Redis()

from rq.decorators import job

from flask import flash


class HrManager:
    def __init__(self):
        pass


    @staticmethod
    def check_if_application_owned_by_user(application_id, user_id):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            application = HrApplication.query.filter_by(id=int(application_id)).first()
            if unicode(application.user_id) == unicode(user_id):
                return True

        return False

