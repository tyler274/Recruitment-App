# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template
from flask_security import SQLAlchemyUserDatastore

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
)
from recruit_app import public, user
from recruit_app.user import admin as admin_view
from recruit_app.user.models import User, Role, roles_users


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
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    #login_manager.init_app(app)
    security.init_app(app, user_datastore)
    debug_toolbar.init_app(app)
    bootstrap.init_app(app)
    rqDashboard.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)

    return None

def register_admin(admin, db):
    # if not Role.query.filter_by(name="admin").first():
    #         a = Role.create(name="admin", description="Admin Role")
    #         u = User.query.filter_by(id=1).first()

    admin_view.register_admin_views(admin, db)

    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
