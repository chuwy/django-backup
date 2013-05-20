=============
django-backup
=============

**WARNING!** This fork of django-backup is experimental and highly unstable.
Do not use it for production.

Also, it has nothing common with parent repos. Soon the name will be changed.

Repository: http://github.com/chuwy/django-backup

Highly extendable and super customizible backup system for Djagno projects.


Installation
------------

At this moment, another fork of django-backup lives on pypi,
so you couldn't install it via pip. Instead, you can clone it and install::

    git clone git@github.com:chuwy/django-backup.git
    cd django-backup
    python setup.py build
    python setup.py install

The add ``django_backup`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'django_backup',
        ..
    )


Core principles
---------------

django-backup has two main concepts for customize backup process:

#. Backupers. Responsible for what you want to backup and how you want to do it.
   For example, you may want to backup only your media, or only your Postgres
   DB, or only few tables from postgres DB, or NoSQL, or...
   At this moment, we have only Postgres Backuper.
#. Savers. Responsible for what you want to do with your backups. For example,
   you may want to store it in local directory, or on remote server, or send it
   to email, or Amazon Glacier, or may be something else.

Backupers and savers have standartized interface, which you can implement by
yourself. `management.py` will just work with this interfaces. Also,
django-backup will contain several most used savers and backupers.

You can choose which savers use for which backups, for example store
DB backup on remote server via SSH, and store your media on Amazon Glacier. It
available via settings.py.

Commands
--------

At this moment, django-backup has only three commands::

    python management.py backup
    python management.py list
    python management.py restore

