# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter
from flask import current_app
import requests

class IaManager:
    def __init__(self):
        pass

    @staticmethod
    def submit_issue(user, subject, body, logs):
        if not current_app.config['TAIGA_USER']:
            return False
    
        issue_text = ""\
            "[Issue Overview]\n" \
            "----------------\n{0}\n\n" \
            "[Issue Story]\n" \
            "-------------\n\n" \
            "[Resolution]\n" \
            "------------\n\n" \
            "[Reporter]\n" \
            "----------\n{1}\n\n" \
            "[Involved Characters]\n" \
            "---------------------\n\n" \
            "[Chat Logs (For submissions only)]\n" \
            "----------------------------------\n{2}".format(body, user.main_character, logs)
    
        s = requests.session()
        headers = {'Content-Type': 'application/json'}
        data = {
            'type':     'normal',
            'username': current_app.config['TAIGA_USER'],
            'password': current_app.config['TAIGA_PASSWORD'],
        }
        req = s.post('https://api.taiga.io/api/v1/auth', headers=headers, json=data)
        
        auth_token = req.json()['auth_token']
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(auth_token),        
        }
        
        proj_id = s.get('https://api.taiga.io/api/v1/resolver?project=kyiera-karmafleet-ia', headers=headers).json()['project']
        # type_ids = s.get('https://api.taiga.io/api/v1/issue-types?project={0}'.format(proj_id), headers=headers).json()
        # u'id': 353277, u'name': u'Member IA Request'
        type_id = 353277
        
        data = {
            'project':      proj_id,
            'subject':      subject,
            'description':  issue_text,
            'type':         type_id,
        }
        resp = s.post('https://api.taiga.io/api/v1/issues', headers=headers, json=data)
        
        return resp.status_code == 201
