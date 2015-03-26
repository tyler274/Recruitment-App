from flask_admin.contrib.sqla import ModelView
from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role, roles_users, AuthInfo

from recruit_app.extensions import user_datastore, db
from flask_security import current_user

from flask import abort


def register_admin_views(admin, db):
    admin.add_view(AuthenticatedModelView(EveCharacter, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(EveCorporationInfo, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(EveAllianceInfo, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(EveApiKeyPair, db.session, category='EvE'))
    admin.add_view(AuthenticatedModelView(User, db.session, endpoint="users", category='Users'))
    admin.add_view(AuthenticatedModelView(Role, db.session, category='Users'))
    admin.add_view(AuthenticatedModelView(AuthInfo, db.session, category='Users'))


def check_if_admin():
    if current_user:
        if current_user.has_role("admin"):
            return True
        else:
            return False
    else:
        return False


class AuthenticatedModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if current_user.has_role("admin"):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            abort(401)
