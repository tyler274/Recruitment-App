from recruit_app.admin import AuthenticatedModelView
from models import BlacklistCharacter, BlacklistGSF

def register_admin_views(admin, db):
    admin.add_view(BlacklistCharacterAdmin(BlacklistCharacter, db.session, category='BlackList'))
    admin.add_view(BlacklistGSFAdmin(BlacklistGSF, db.session, name='GSF Blacklist Cache', category='BlackList'))

# Useful things: column_list, column_labels, column_searchable_list, column_filters, form_columns, form_ajax_refs
class BlacklistCharacterAdmin(AuthenticatedModelView):
    column_searchable_list = (
        'name',
        'main_name',
        'corporation',
        'alliance',
        'notes',
        'ip_address',
        'creator.email', )
    column_labels = {
        'creator.email': 'Creator', }
    column_list = column_searchable_list
    column_filters = column_list
    form_ajax_refs = {
        'creator': { 'fields': ('email', ) }, }


class BlacklistGSFAdmin(AuthenticatedModelView):
    column_searchable_list = (
        'character.character_name',
        'status', )
    column_filters = column_searchable_list + ('created_time', 'last_update_time', )
    form_ajax_refs = {
        'character': { 'fields': ('character_name', ) }, }
