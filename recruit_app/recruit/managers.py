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

    @staticmethod
    def create_comment(application_id, comment, user_id):
        comment = HRApplicationComment()
        comment.application_id = application_id
        comment.user_id = user_id
        comment.comment = comment
        comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def alter_application(application_id, action, user_id):
        if HrApplication.query.filter_by(id=int(application_id)).first():
            application = HrApplication.query.filter_by(id=int(application_id)).first()

            if action == "approve":
                application.approved_denied = "Approved"
                application.reviewer_user_id = user_id
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "approved"

            elif action == "reject":
                application.approved_denied = "Rejected"
                application.reviewer_user_id = user_id
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "rejected"

            elif action == "pending":
                application.approved_denied = "Pending"
                application.reviewer_user_id = user_id
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "pending"

            elif action == "undecided":
                application.approved_denied = "undecided"
                application.reviewer_user_id = user_id
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "undecided"

            elif action == "delete":
                application.delete()
                return "deleted"

