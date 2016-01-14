from flask import Blueprint, render_template
from flask_security.decorators import login_required
from flask_security import current_user, roles_accepted

from recruit_app.hr.managers import HrManager

blueprint = Blueprint("hr", __name__, url_prefix='/hr', static_folder="../static")

@blueprint.route("/compliance/<int:corp_id>", methods=['GET'])
@login_required
@roles_accepted('admin', 'compliance')
def compliance(corp_id):
    return render_template('hr/compliance.html', data=HrManager.get_compliance(corp_id))
