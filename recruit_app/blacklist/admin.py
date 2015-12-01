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
        'ip_address', )
    
    column_list = column_searchable_list + ('creator', )
    column_filters = column_list
    form_ajax_refs = {
        'creator': { 'fields': ('email', ) }, }


class BlacklistGSFAdmin(AuthenticatedModelView):
    form_ajax_refs = {
        'character': { 'fields': ('character_name', ) }, }
