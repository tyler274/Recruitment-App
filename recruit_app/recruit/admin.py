from recruit_app.recruit.models import HrApplication, HrApplicationComment
from recruit_app.user.models import EveCharacter

from recruit_app.admin import AuthenticatedModelView


def register_admin_views(admin, db):
    admin.add_view(HrApplicationAdmin(HrApplication, db.session, category='Recruitment'))
    admin.add_view(AuthenticatedModelView(HrApplicationComment, db.session, category='Recruitment'))
    # admin.add_view(AuthenticatedModelView(EveCorporationInfo, db.session, category='EvE'))
    # admin.add_view(AuthenticatedModelView(EveAllianceInfo, db.session, category='EvE'))
    # admin.add_view(AuthenticatedModelView(EveApiKeyPair, db.session, category='EvE'))
    # admin.add_view(AuthenticatedModelView(User, db.session, endpoint="users", category='Users'))
    # admin.add_view(AuthenticatedModelView(Role, db.session, category='Users'))


class HrApplicationAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    # column_searchable_list = (HrApplication.how_long, 'user.characters.character_name')
    column_filters = ('how_long', 'thesis')

    # def init_search(self):
    #     r = super(HrApplicationAdmin, self).init_search()
    #     print self._search_joins