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

    u = User.query.filter_by(id=1).first()
    r = Role.query.filter_by(id=1).first()
    u.roles.append(r)
    db.session.add(u)
    db.session.commit()

    def is_accessible(self):

        if current_user.has_role("admin"):
            return True
        return False
