# -*- coding: utf-8 -*-
from recruit_app.user.models import EveCharacter
from recruit_app.extensions import cache
from flask import current_app
import requests
from bs4 import BeautifulSoup

class HrManager:
    def __init__(self):
        pass

    @staticmethod
    @cache.cached(timeout=3600, key_prefix='get_compliance')
    def get_compliance(corp_id):
        url = 'https://goonfleet.com'

        s = requests.session()
        r = s.get(url, verify=True)

        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', {'name':'auth_key'})['value']
        
        payload = {
            'ips_username' : current_app.config['GSF_USERNAME'],
            'ips_password' : current_app.config['GSF_PASSWORD'],
            'auth_key' : token,
            'referer' : 'https://goonfleet.com/',
            'rememberMe' : 1,
        }

        url = 'https://goonfleet.com/index.php?app=core&module=global&section=login&do=process'
        r = s.post(url, data=payload, verify=True)
        
        url = 'https://goonfleet.com/corps/checkMembers.php'
        r = s.get(url, verify=True)
        
        payload = {
            'corpID' : str(corp_id)
        }
        r = s.post(url, data=payload, verify=True)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        output = "<table id='compliance' class='table tablesorter'><thead><th>Character Name</th><th>Forum Name/Main</th><th>Primary Group</th><th>Status</th></thead><tbody>\n"
        
        for row in soup.findAll('tr'):
            alert = None
            if row.get('class'):
                alert = row.get('class')[1]
            cols = row.findAll('td')
            charname = cols[1].get_text()
            forumname = cols[2].get_text()
            group = cols[3].get_text()
            
            # Look for an API for character
            if not alert and not EveCharacter.query.filter_by(character_name=charname).first():
                alert = 'alert-warning'
                
            # Set status
            if alert == 'alert-warning':
                status = 'No KF API'
            elif alert == 'alert-success':
                status = 'Director'
            elif alert == 'alert-error':
                status = 'No Goon Auth'
            else:
                status = 'OK'
                
            if alert:
                output = output + '<tr class="alert {0}"><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>\n'.format(alert, charname, forumname, group, status)
            else:
                output = output + '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>\n'.format(charname, forumname, group, status)
        
        output = output + '</tbody></table>'
        return output
