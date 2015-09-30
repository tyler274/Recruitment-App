# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# from flask_login import LoginManager
# login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_security import Security, SQLAlchemyUserDatastore
from recruit_app.user.models import User, Role
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# from flask_login import LoginManager
# login_manager = LoginManager()

from flask_migrate import Migrate
migrate = Migrate()

# import logging
from raven.contrib.flask import Sentry
sentry = Sentry()

from flask_cache import Cache
cache = Cache()

from flask_debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

from rq_dashboard import RQDashboard
from recruit_app.user.admin import check_if_admin
rqDashboard = RQDashboard(auth_handler=check_if_admin)

from flask_admin import Admin
admin = Admin()

from flask_mail import Mail
mail = Mail()

from flask_rq import RQ
rq = RQ()

from flask_misaka import Misaka
misaka = Misaka()
