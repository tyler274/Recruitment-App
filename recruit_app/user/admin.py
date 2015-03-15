from flask_admin.contrib.sqla import ModelView
from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role, roles_users

from recruit_app.extensions import user_datastore, db
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
        if not Role.query.filter_by(name="admin").first():
            a = Role.create(name="admin", description="Admin Role")
            ru = roles_users('1','1')
            db.session.add(ru)
            db.session.commit()


        if current_user.has_role("admin"):
            return True
        return False
