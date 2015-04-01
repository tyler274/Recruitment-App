import os
import urlparse
from redis import Redis
from rq import Worker, Queue, Connection

from recruit_app.app import create_app
from recruit_app.settings import DevConfig, ProdConfig

listen = ['high', 'medium', 'low']

redis_url = os.getenv('REDISTOGO_URL')
# if not redis_url:
#     raise RuntimeError('Set up Redis To Go first.')

if redis_url:
    urlparse.uses_netloc.append('redis')
    url = urlparse.urlparse(redis_url)
    conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)
else:
    conn = Redis()

if __name__ == '__main__':
    if os.environ.get("RECRUIT_APP_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)

    with app.app_context():
        with Connection(conn):
            worker = Worker(map(Queue, listen))
            worker.work()
