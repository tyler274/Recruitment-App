# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter, EveApiKeyPair, EveAllianceInfo, EveCorporationInfo, AuthInfo, User

from recruit_app.recruit.models import HrApplication, HrApplicationComment

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
    def create_comment(application_id, comment_data, user_id):
        comment = HrApplicationComment()
        comment.application_id = application_id
        comment.comment = comment_data
        comment.user_id = user_id
        comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def create_application(how_long, have_done, scale, reason_for_joining, favorite_ship, favorite_role, most_fun, main_character_name, user_id, characters):
        application = HrApplication()
        application.how_long = how_long
        application.have_done = have_done
        application.scale = scale
        application.reason_for_joining = reason_for_joining
        application.favorite_ship = favorite_ship
        application.favorite_role = favorite_role
        application.most_fun = most_fun
        application.user_id = user_id

        for character in characters:
                eve_character = EveCharacter.query.filter_by(character_id=character).first()
                application.characters.append(eve_character)

        application.main_character_name = main_character_name
        application.last_update_time = dt.datetime.utcnow()
        application.save()


    @staticmethod
    def update_application(how_long, have_done, scale, reason_for_joining, favorite_ship, favorite_role, most_fun, application_id, main_character_name, user_id, characters):
        if HrApplication.query.filter_by(id=application_id).first():
            application = HrApplication.query.filter_by(id=application_id).first()
            application.how_long = how_long
            application.have_done = have_done
            application.scale = scale
            application.reason_for_joining = reason_for_joining
            application.favorite_ship = favorite_ship
            application.favorite_role = favorite_role
            application.most_fun = most_fun
            application.user_id = user_id

            for character in characters:
                eve_character = EveCharacter.query.filter_by(character_id=character).first()
                application.characters.append(eve_character)

            application.main_character_name = main_character_name
            application.last_update_time = dt.datetime.utcnow()
            application.save()

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
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "pending"

            elif action == "undecided":
                application.approved_denied = "Undecided"
                application.last_user_id = user_id
                application.last_update_time = dt.datetime.utcnow()
                application.save()
                return "undecided"

            elif action == "delete":
                application.delete()
                return "deleted"