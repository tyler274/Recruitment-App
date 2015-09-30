web: gunicorn recruit_app.wsgi:app -b 0.0.0.0:$PORT --log-syslog-to tcp://logs3.papertrailapp.com:19139
# worker: python -u run-worker.py
# scheduler: python -u run-scheduler.py -i 1 autostart=true autorestart=true stopsignal=TERM
