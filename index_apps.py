#!/usr/bin/env python

import os
import sys
from recruit_app.app import create_app
from recruit_app.settings import DevConfig, ProdConfig
from recruit_app.recruit.models import HrApplication as Model
from flask.ext.whooshalchemy import whoosh_index

sys.stdout  = os.fdopen(sys.stdout.fileno(), 'w', 0)
atatime     = 512

if __name__ == '__main__':
    if os.environ.get("RECRUIT_APP_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)

    with app.app_context():
        index       = whoosh_index(app, Model)
        searchable  = Model.__searchable__
        print 'counting rows...'
        total       = int(Model.query.order_by(None).count())
        done        = 0
        print 'total rows: {}'.format(total)
        writer = index.writer(limitmb=10000, procs=16, multisegment=True)
        for p in Model.query.yield_per( atatime ):
            record = dict([(s, p.__dict__[s]) for s in searchable])
            record.update({'id' : unicode(p.id)}) # id is mandatory, or whoosh won't work
            writer.add_document(**record)
            done += 1
            if done % atatime == 0:
                print 'c {}/{} ({}%)'.format(done, total, round((float(done)/total)*100,2) ),

        print '{}/{} ({}%)'.format(done, total, round((float(done)/total)*100,2) )
        writer.commit()