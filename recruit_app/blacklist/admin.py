from recruit_app.admin import AuthenticatedModelView
from models import BlacklistCharacter


def register_admin_views(admin, db):
    # admin.add_view(HrBlacklistAdmin(HrBlacklist, db.session, category='BlackList'))
    admin.add_view(BlacklistCharacterAdmin(BlacklistCharacter, db.session, category='BlackList'))


class BlacklistCharacterAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    column_filters = ('alliance', 'main_name', 'corporation', 'ip_address', 'name', 'notes')
