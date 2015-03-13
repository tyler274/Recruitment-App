from flask_admin.contrib.sqla import ModelView
from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role

from flask_login import login_required, current_user


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
        u = User.query.filter_by(user_id=current_user.get_id()).first()
        return current_user.is_authenticated()
