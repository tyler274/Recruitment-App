from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from flask import abort


class AuthenticatedModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if current_user.has_role("admin"):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            abort(401)
