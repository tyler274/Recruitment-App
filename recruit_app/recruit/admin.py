from recruit_app.recruit.models import HrApplication, HrApplicationComment

from recruit_app.admin import AuthenticatedModelView


def register_admin_views(admin, db):
    admin.add_view(HrApplicationAdmin(HrApplication, db.session, category='Recruitment'))
    admin.add_view(AuthenticatedModelView(HrApplicationComment, db.session, category='Recruitment'))


class HrApplicationAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    # column_searchable_list = (HrApplication.how_long, 'user.characters.character_name')
    column_filters = ('how_long', 'thesis')

    # def init_search(self):
    #     r = super(HrApplicationAdmin, self).init_search()
    #     print self._search_joins