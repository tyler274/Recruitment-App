https://travis-ci.org/tyler274/Recruitment-App.svg?branch=master
===============================
recruit
===============================

A Corporation platform for EvE Online, currently features a recruitment system (tailored to KarmaFleet and Goonswarm) with incoming features including a blacklist and member tracking, among other things.

This is not intended to compete with tools like ECM (https://github.com/evecm/ecm) but will share some features and concepts. 


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export RECRUIT_APP_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/tyler274/recruit_app
    cd recruit_app
    pip install -r requirements/dev.txt
    python manage.py server

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration:

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``RECRUIT_APP_ENV`` environment variable is set to ``"prod"``.

Don't forget to define your postgresql db using

::

    export DATABASE_URL="postgres://username:password@domain-name:5432/database-name"

Define your gmail username and pass environment variables
::

    export MAIL_USERNAME="gmail_username"
    export MAIL_PASSWORD="gmail_password"

Shell
-----

To open the interactive shell, run ::

    python manage.py shell


Make sure to add the admin role to a user
::
    from recruit_app.user.models import User, Role
    u = User.query.filter_by(id="1").first()
    r = Role(name="admin", description="administrator")
    u.roles.append(r)
    u.save()

By default, you will have access to ``app``, ``db``, ``Role``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
