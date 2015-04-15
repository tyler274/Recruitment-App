# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from recruit_app.settings import ProdConfig
from recruit_app.assets import assets
from recruit_app.extensions import (
    bcrypt,
    cache,
    db,
    #login_manager,
    security,
    user_datastore,
    migrate,
    debug_toolbar,
    bootstrap,
    rqDashboard,
    admin,
    mail,
    rq,
)
from recruit_app import public, user, recruit
from recruit_app.user import admin as user_admin_view
from recruit_app.recruit import admin as recruit_admin_view
from recruit_app.recruit import search as recruit_search
from recruit_app.public.forms import ConfirmRegisterFormRecaptcha

from recruit_app.scheduled_tasks import schedule_tasks
from redis import Redis

from sqlalchemy_searchable import make_searchable


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_admin(admin, db)
    register_search(app)
    register_tasks()

    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    make_searchable()
    #login_manager.init_app(app)
    security.init_app(app, user_datastore, register_blueprint=True, confirm_register_form=ConfirmRegisterFormRecaptcha)
    debug_toolbar.init_app(app)
    bootstrap.init_app(app)
    rqDashboard.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    rq.init_app(app)
    migrate.init_app(app, db)

    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(recruit.views.blueprint)

    return None


def register_admin(admin, db):
    user_admin_view.register_admin_views(admin, db)
    recruit_admin_view.register_admin_views(admin, db)

    return None


def register_tasks():
    # schedule_tasks()

    return None


def register_search(app):
    # recruit_search.register_search_models(app)

    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
