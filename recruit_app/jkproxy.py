from flask import Blueprint, request, current_app, flash, redirect, url_for
from flask_security.decorators import login_required
from flask_security import roles_accepted, current_user
from recruit_app.user.eve_api_manager import EveApiManager
from recruit_app.user.models import EveApiKeyPair
from flask import Response
from flask import stream_with_context

import re
import requests

blueprint = Blueprint("eveapi", __name__, url_prefix='/eveapi')

@blueprint.route("/audit.php", methods=['GET'])
@login_required
@roles_accepted('admin', 'recruiter', 'reviewer', 'compliance')
def jackknife_proxy():
    # Remove any passed in apik and redirect back without it
    if 'apik' in request.args:
        cleanargs = request.args.copy()
        cleanargs.pop('apik')
        return redirect(url_for('eveapi.jackknife_proxy', **cleanargs))
    
    try:
        api_key = EveApiKeyPair.query.filter_by(api_id=request.args['usid']).first().api_key
    except:
        return 'API key not in database.'
        
    if 'chid' in request.args and not (current_user.has_role("admin") or current_user.has_role("recruiter") or current_user.has_role("compliance")):
        chid = request.values['chid']
        
        if EveApiManager.check_if_character_is_in_corp(int(chid), 98370861):
            return 'Insufficient permissions to view KarmaFleet character page.'
        
    #import ipdb; ipdb.set_trace()
    
    url = current_app.config['JACK_KNIFE_URL'] + '?' + request.query_string + '&apik=' + api_key
    headers = { 'User-Agent': 'KarmaFleet API Check', 'From': 'karmafleet_tools@ggrog.com' } # Be nice to Jackknife and send some info about us
    req = requests.get(url, stream = True, headers=headers)
    
    # Some python generator magic to intercept each line and sanitize API keys, and redirect links back to audit.php with ours
    def streamJackknife():
        for line in req.iter_lines():
            line = re.sub(current_app.config['JACK_KNIFE_URL'], 'audit.php', line)
            line = re.sub('apik=[^&#"]*&?', '', line)
            line = re.sub('http://ajax\.googleapis\.com', 'https://ajax.googleapis.com', line) # need to switch to secure js
            yield line + '\n'
        
    return Response(stream_with_context(streamJackknife()))
