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
    def check_if_application_owned_by_user(application_id, user):
        application = HrApplication.query.filter_by(id=application_id).first()
        if application:
            if application.user_id == user.id:
                return True

        return False

    @staticmethod
    def create_comment(application, comment_data, user):
        comment = HrApplicationComment()
        comment.application_id = application.id
        comment.comment = comment_data
        comment.user_id = user.id
        comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def edit_comment(comment, comment_data):
        comment.comment = comment_data
        comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def create_application(how_long, have_done, scale, reason_for_joining, favorite_ship, favorite_role, most_fun, main_character_name, user, characters):
        application = HrApplication()
        application.how_long = how_long
        application.have_done = have_done
        application.scale = scale
        application.reason_for_joining = reason_for_joining
        application.favorite_ship = favorite_ship
        application.favorite_role = favorite_role
        application.most_fun = most_fun
        application.hidden = False
        application.user_id = user.id

        for character in characters:
                # The form data for characters selected is the character id
                eve_character = EveCharacter.query.filter_by(character_id=character).first()
                application.characters.append(eve_character)

        application.main_character_name = main_character_name
        application.last_update_time = dt.datetime.utcnow()
        application.save()


    @staticmethod
    def update_application(how_long,
                           have_done,
                           scale,
                           reason_for_joining,
                           favorite_ship,
                           favorite_role,
                           most_fun,
                           application,
                           main_character_name,
                           user,
                           characters):

        application = HrApplication.query.filter_by(id=application.id).first()
        application.how_long = how_long
        application.have_done = have_done
        application.scale = scale
        application.reason_for_joining = reason_for_joining
        application.favorite_ship = favorite_ship
        application.favorite_role = favorite_role
        application.most_fun = most_fun
        application.user_id = user.id

        for character in characters:
            eve_character = EveCharacter.query.filter_by(character_id=character).first()
            application.characters.append(eve_character)

        application.main_character_name = main_character_name
        application.last_update_time = dt.datetime.utcnow()
        application.save()

    @staticmethod
    def alter_application(application, action, user):
        if action == "approve":
            application.approved_denied = "Approved"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "approved"

        elif action == "reject":
            application.approved_denied = "Rejected"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "rejected"

        elif action == "pending":
            application.approved_denied = "Pending"
            application.last_user_id = user.id
            application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "pending"

        elif action == "undecided":
            application.approved_denied = "Undecided"
            application.last_user_id = user.id
            application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "undecided"

        elif action == "hide":
            application.hidden = True
            application.save()
            return "hidden"

        elif action == "delete":
            application.delete()
            return "deleted"