from flask_admin.contrib.sqla import ModelView
from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role, roles_users

from recruit_app.extensions import user_datastore, db
from flask_security import current_user


def register_admin_views(admin, db):
    admin.add_view(AuthenticatedModelView(EveCharacter, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(EveCorporationInfo, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(EveAllianceInfo, db.session, category='Eve'))
    admin.add_view(AuthenticatedModelView(EveApiKeyPair, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(User, db.session, endpoint="users", category='Users'))
    admin.add_view(AuthenticatedModelView(Role, db.session, category='Users'))

class AuthenticatedModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if current_user.has_role("admin"):
            return True
        return False
