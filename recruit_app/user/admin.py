from flask_admin.contrib.sqla import ModelView
from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role

from recruit_app.extensions import user_datastore
from flask_security import current_user


def register_admin_views(admin, db):
    admin.add_view(AuthenticatedModelView(EveCharacter, db.session))
    admin.add_view(AuthenticatedModelView(EveCorporationInfo, db.session))
    admin.add_view(AuthenticatedModelView(EveAllianceInfo, db.session))
    admin.add_view(AuthenticatedModelView(EveApiKeyPair, db.session))
    admin.add_view(AuthenticatedModelView(User, db.session, endpoint="users"))
    admin.add_view(AuthenticatedModelView(Role, db.session))

class AuthenticatedModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        user_datastore.create_role(name="admin", description="Admin Role")
        u = User.query.filter_by(id=current_user.get_id()).first()
        r = Role.query.filter_by(name="admin").first()
        user_datastore.add_role_to_user(u, r)
        if u.has_role(r):
            return True
        return False
