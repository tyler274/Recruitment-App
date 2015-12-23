from flask import Blueprint, request, current_app, flash, redirect
from flask_security.decorators import login_required
from flask_security import roles_accepted

from recruit_app.user.models import EveApiKeyPair
from flask import Response
from flask import stream_with_context

import re
import requests

blueprint = Blueprint("eveapi", __name__, url_prefix='/eveapi')#, static_folder=".")

@blueprint.route("/audit.php", methods=['GET'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer', 'compliance')
def jackknife_proxy():
    try:
        api_key = EveApiKeyPair.query.filter_by(api_id=request.args['usid']).first().api_key
    except:
        flash('API key not in database.', 'error')
        return redirect(request.referrer)
    
    url = current_app.config['JACK_KNIFE_URL'] + '?' + request.query_string + '&apik=' + api_key
    headers = { 'User-Agent': 'KarmaFleet API Check', 'From': 'karmafleet_tools@ggrog.com' } # Be nice to Jackknife and send some info about us
    req = requests.get(url, stream = True, headers=headers)
    
    # Some python generator magic to intercept each line and sanitize API keys, and redirect links back to audit.php with ours
    def streamJackknife():
        for line in req.iter_lines():
            rem_jk = re.sub(current_app.config['JACK_KNIFE_URL'], 'audit.php', line)
            rem_apikey = re.sub('apik=[^&#"]*&?', '', rem_jk)
            yield rem_apikey + '\n'
        
    return Response(stream_with_context(streamJackknife()))
