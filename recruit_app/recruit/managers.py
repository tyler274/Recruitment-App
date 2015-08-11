# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter

from recruit_app.recruit.models import HrApplication, HrApplicationComment

import datetime as dt

from recruit_app.user.eve_api_manager import EveApiManager

from recruit_app.extensions import bcrypt, cache

from flask import flash, current_app
import requests
from bs4 import BeautifulSoup

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
    @cache.cached(timeout=3600, key_prefix='get_compliance')
    def get_compliance():
        url = 'https://goonfleet.com'

        s = requests.session()
        r = s.get(url, verify=True)

        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', {'name':'auth_key'})['value']
        
        payload = {
        'ips_username' : current_app.config['GSF_USERNAME'],
        'ips_password' : current_app.config['GSF_PASSWORD'],
        'auth_key' : token,
        'referer' : 'https://goonfleet.com/',
        'rememberMe' : 1,
        }

        url = 'https://goonfleet.com/index.php?app=core&module=global&section=login&do=process'
        r = s.post(url, data=payload, verify=True)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        url = 'https://goonfleet.com/corps/checkMembers.php'
        r = s.get(url, verify=True)
        
        payload = {
        'corpID' : '98370861'
        }
        r = s.post(url, data=payload, verify=True)
        
        d = r.text.split('<div class="row-fluid">')[2].split('</div>')[2]
        return d

    @staticmethod
    def create_comment(application, comment_data, user):
        comment = HrApplicationComment()
        comment.application_id = application.id
        comment.comment = comment_data
        comment.user_id = user.id
        # comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def edit_comment(comment, comment_data):
        comment.comment = comment_data
        comment.last_update_time = dt.datetime.utcnow()
        comment.save()

    @staticmethod
    def create_application(form, main_character_name, user):
        application = HrApplication()
        application.alt_application = form.alt_application.data
        application.how_long = form.how_long.data
        application.notable_accomplishments = form.notable_accomplishments.data
        application.corporation_history = form.corporation_history.data
        application.why_leaving = form.why_leaving.data
        application.what_know = form.what_know.data
        application.what_expect = form.what_expect.data
        application.bought_characters = form.bought_characters.data
        application.why_interested = form.why_interested.data

        application.goon_interaction = form.goon_interaction.data
        application.friends = form.friends.data

        #application.reason_for_joining = form.reason_for_joining.data
        application.find_out = form.find_out.data
        application.favorite_role = form.favorite_role.data
        application.thesis = form.thesis.data

        application.scale = form.scale.data

        application.hidden = False
        application.user_id = user.id

        for character in form.characters.data:
                # The form data for characters selected is the character id
                eve_character = EveCharacter.query.filter_by(character_id=character).first()
                application.characters.append(eve_character)

        application.main_character_name = main_character_name
        # application.last_update_time = dt.datetime.utcnow()
        application.save()

        return application


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
        # application.last_update_time = dt.datetime.utcnow()
        application.save()

    @staticmethod
    def alter_application(application, action, user):
        if action == "approve":
            application.approved_denied = "Approved"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "approved"

        elif action == "reject":
            application.approved_denied = "Rejected"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "rejected"

        # elif action == "pending":
        #     application.approved_denied = "Pending"
        #     application.last_user_id = user.id
        #     application.last_update_time = dt.datetime.utcnow()
        #     application.save()
        #     return "pending"

        elif action == "undecided":
            application.approved_denied = "Undecided"
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "undecided"

        elif action == "stasis":
            application.approved_denied = "Role Stasis"
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "Role Stasis"

        elif action == "director_review":
            application.approved_denied = "Needs Director Review"
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "Needs Director Review"

        elif action == "waiting":
            application.approved_denied = "Awaiting Response"
            application.last_user_id = user.id
            # application.last_update_time = dt.datetime.utcnow()
            application.save()
            return "Awaiting Response"

        elif action == "hide":
            application.hidden = True
            application.save()
            return "hidden"

        elif action == "unhide":
            application.hidden = False
            application.save()
            return "unhidden"

        elif action == "delete":
            application.delete()
            return "deleted"

        elif action == 'close':
            application.approved_denied = 'Closed'
            application.save()
            return 'Closed'
