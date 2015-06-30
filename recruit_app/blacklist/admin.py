from recruit_app.admin import AuthenticatedModelView
from models import BlacklistCharacter


def register_admin_views(admin, db):
    # admin.add_view(HrBlacklistAdmin(HrBlacklist, db.session, category='BlackList'))
    admin.add_view(BlacklistCharacterAdmin(BlacklistCharacter, db.session, category='BlackList'))

# class HrBlacklistAdmin(AuthenticatedModelView):
#     column_auto_select_related = True
#     # column_display_all_relations = True
#     # column_searchable_list = (HrApplication.how_long, 'user.characters.character_name')
#     column_filters = ('comment', 'known_characters', 'user', 'creator')
#
#     # def init_search(self):
#     #     r = super(HrApplicationAdmin, self).init_search()
#     #     print self._search_joins

class BlacklistCharacterAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    column_filters = ('alliance', 'main_name', 'corporation', 'name', 'notes')
