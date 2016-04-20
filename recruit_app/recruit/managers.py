# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter

from recruit_app.recruit.models import HrApplication, HrApplicationComment, HrApplicationCommentHistory

import datetime as dt

from flask import current_app, url_for
import requests
import re

class RecruitManager:
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
        if user:
            comment.user_id = user.id
        comment.save()
        application.last_update_time = dt.datetime.utcnow()
        application.save()
        RecruitManager.comment_notify(comment)

    @staticmethod
    def edit_comment(comment, comment_data, user):
        # Save the previous version of the comment for possible future use / auditing
        comment_history = HrApplicationCommentHistory()
        comment_history.old_comment = comment.comment
        comment_history.comment_id = comment.id
        comment_history.editor = user
        comment_history.save()

        # Save the edit
        comment.comment = comment_data
        comment.last_update_time = dt.datetime.utcnow()
#        if not comment.user_id:
#            comment.user = user
        comment.application.last_update_time = dt.datetime.utcnow()
        comment.save()
        RecruitManager.comment_notify(comment)

    @staticmethod
    def create_application(form, user):
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

        application.main_character_name = user.main_character.character_name
        # application.last_update_time = dt.datetime.utcnow()

        application.save()
        RecruitManager.application_action_notify(application, 'new')
        
        # Create a starter comment
        comment_text = "#### Accounts as of " + application.created_time.strftime('%Y/%m/%d %H:%M') + ":\n"
        for api_key in application.user.api_keys:
            comment_text += api_key.api_id + "\n\n"
            for character in api_key.characters:
                comment_text += "- " + character.character_name + "\n"
            comment_text += "\n"
        RecruitManager.create_comment(application, comment_text, 0)

        return application


    @staticmethod
    def alter_application(application, action, user):
        retval = 'unknown application action'
        if action == "approve":
            application.approved_denied = "Approved"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            application.training = False
            application.save()
            retval = "Approved"

        elif action == "reject":
            application.approved_denied = "Rejected"
            application.reviewer_user_id = user.id
            application.last_user_id = user.id
            application.training = False
            application.save()
            retval = "Rejected"

        elif action == 'new':
            application.approved_denied = 'New'
            application.last_user_id = user.id
            application.save()
            retval = 'New'

        elif action == "undecided":
            application.approved_denied = "Undecided"
            application.last_user_id = user.id
            application.save()
            retval = "Undecided"

        elif action == "stasis":
            application.approved_denied = "Role Stasis"
            application.last_user_id = user.id
            application.save()
            retval = "Role Stasis"

        elif action == "director_review":
            application.approved_denied = "Needs Director Review"
            application.last_user_id = user.id
            application.save()
            retval = "Needs Director Review"

        elif action == "waiting":
            application.approved_denied = "Awaiting Response"
            application.last_user_id = user.id
            application.save()
            retval = "Awaiting Response"

        elif action == "hide":
            application.hidden = True
            application.last_user_id = user.id
            application.save()
            retval = "hidden"

        elif action == "unhide":
            application.hidden = False
            application.last_user_id = user.id
            application.save()
            retval = "unhidden"

        elif action == "delete":
            application.delete()
            retval = "deleted"

        elif action == 'close':
            application.approved_denied = 'Closed'
            application.last_user_id = user.id
            application.training = False
            application.save()
            retval = 'Closed'

        elif action == 'needs_processing':
            application.approved_denied = 'Needs Processing'
            application.last_user_id = user.id
            application.save()
            retval = 'Needs Processing'

        elif action == 'missing_ingame':
            application.approved_denied = 'Missing In-Game'
            application.last_user_id = user.id
            application.save()
            retval = 'Missing In-Game'
            
        elif action == 'training':
            application.training = not application.training;
            application.save()
            if application.training:
                retval = 'is now a training application and will be shown first'
            else:
                retval = 'is no longer a training app'

        RecruitManager.application_action_notify(application, action)
        return retval

    @staticmethod
    def application_action_notify(application, action):
        # Send a request to slack
#            if action == 'new':
#                message_text = "New application from {0}: {1}".format(application.main_character_name, url_for('recruit.application_view', _external=True, application_id=application.id))
        if action == 'needs_processing':
            message_text = "Application from {0} needs processing: {1}".format(application.main_character_name, url_for('recruit.application_view', _external=True, application_id=application.id))
        elif action == 'director_review':
            message_text = "Application from {0} needs director review: {1}".format(application.main_character_name, url_for('recruit.application_view', _external=True, application_id=application.id))

        # Send the message
        try:
            RecruitManager.send_slack_notification(message_text)
        except:
            pass

    @staticmethod
    def comment_notify(comment):
        # Find all instances of @xxxx text and send slack notifications to those users.  If the user doesn't exist slack will just ignore.
        for ping in re.findall('(?:^|\s)(@\w+)', comment.comment):
            message = "You were mentioned in an application comment: {0}".format(url_for('recruit.application_view', _external=True, application_id=comment.application_id, _anchor="comment{0}".format(comment.id)))
            RecruitManager.send_slack_notification(message, ping)

    @staticmethod
    def send_slack_notification(message, channel=None):
        try:
            data = { 'text': message }
            if channel is not None:
                data['channel'] = channel
            headers = {'Content-Type': 'application/json'}
            requests.post(current_app.config['SLACK_WEBHOOK'], json=data, headers=headers)
        except:
            pass
