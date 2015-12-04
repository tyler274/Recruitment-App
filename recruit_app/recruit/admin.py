from recruit_app.recruit.models import HrApplication, HrApplicationComment, HrApplicationCommentHistory
from recruit_app.user.models import EveCharacter

from recruit_app.admin import AuthenticatedModelView


def register_admin_views(admin, db):
    admin.add_view(HrApplicationAdmin(HrApplication, db.session, category='Recruitment'))
    admin.add_view(HrApplicationCommentAdmin(HrApplicationComment, db.session, category='Recruitment'))
    admin.add_view(HrApplicationCommentHistoryAdmin(HrApplicationCommentHistory, db.session, category='Recruitment'))

# Useful things: column_list, column_labels, column_searchable_list, column_filters, form_columns, form_ajax_refs

class HrApplicationAdmin(AuthenticatedModelView):
    column_list = (
        'id',
        'main_character_name',
        'user',
        'alt_application',
        'created_time',
        #'characters',
        'approved_denied',
        'reviewer_user',
        'last_action_user', )
    column_labels = {
        'main_character_name': 'Main',
        'alt_application': 'Alt?',
        'approved_denied': 'Status',
        'reviewer_user': 'Reviewer',
        'last_action_user': 'Last Action', }
    column_searchable_list = (
        'main_character_name',
        'user.email',
        'characters.character_name',
        'thesis',
        'how_long',
        'notable_accomplishments',
        'corporation_history',
        'why_leaving',
        'what_know',
        'what_expect',
        'bought_characters',
        'why_interested',
        'find_out',
        'favorite_role', )
    column_filters = (
        'id',
        'main_character_name',
        'user.email',
        'alt_application',
        'created_time',
        'approved_denied',
        'reviewer_user.email',
        'last_action_user.email', )
    form_columns = column_list + (
        'created_time',
        'last_update_time',
        'thesis',
        'how_long',
        'notable_accomplishments',
        'corporation_history',
        'why_leaving',
        'what_know',
        'what_expect',
        'bought_characters',
        'why_interested',
        'find_out',
        'favorite_role',
        'characters',
        'hidden', )
    form_ajax_refs = {
        'user':             { 'fields': ('email', ) },
        'reviewer_user':    { 'fields': ('email', ) },
        'last_action_user': { 'fields': ('email', ) },
        'characters':       { 'fields': ('character_name', ) }, }


class HrApplicationCommentAdmin(AuthenticatedModelView):
    column_list = (
        'id',
        'application.id',
        'application.main_character_name',
        'user',
        'comment',
        'created_time',
        'last_update_time', )
    column_labels = {
        'application.main_character_name' : 'Application',
        'application.id' : 'App ID', }
    column_filters = (
        'id',
        'application.id',
        'application.main_character_name',
        'user.email',
        'created_time',
        'last_update_time')
    column_searchable_list = (
        'user.email',
        'application.main_character_name',
        'comment', )
    form_columns = (
        'id',
        'created_time',
        'last_update_time',
        'user',
        'application',
        'comment', )
    form_ajax_refs = {
        'user':        { 'fields': ('email', ) },
        'application': { 'fields': ('main_character_name', ) }, }


class HrApplicationCommentHistoryAdmin(AuthenticatedModelView):
    column_list = (
        'id',
        'comment.id',
        'comment.application_id',
        'old_comment',
        'user',
        'created_time' )
    column_labels = {
        'comment.id' : 'Current Comment ID',
        'comment.application_id' : 'App ID', }
    column_searchable_list = (
        'old_comment',
        'user.email', )
    column_filters = (
        'id',
        'comment.id',
        'user.email',
        'created_time', )
    form_columns = (
        'id',
        'user',
        'created_time',
        'last_update_time',
        'old_comment',
        'comment', )
    form_ajax_refs = {
        'user':    { 'fields': ('email', ) },
        'comment': { 'fields': ('id', 'user', ) }, }

