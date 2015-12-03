__author__ = 'tyler274'
from recruit_app.app import create_app

app = create_app()

#@app.before_request
#def maintenance_mode():
#    return "Site temporarily down for scheduled maintenance.  We'll be back at 04:00 UTC", 503
