#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import tempfile

from django.conf import settings


class PostgresBackup(object):
    def pack(self):
        db = getattr(settings, 'DATABASES')['default']
        filename = os.path.join(self.tmp_catalog, 'db.sql')
        command_tmpl = 'pg_dump -o -w -Fc -Z 7 -U {USER} -C -f {FILE} {NAME}'
        command = command_tmpl.format(
            USER=db['USER'],
            NAME=db['NAME'],
            FILE=filename)
        subprocess.Popen(command.split()).wait()
        self.db = filename

    def create_tmp(self):
        self.tmp_catalog = tempfile.mkdtemp()

    def clean_tmp(self):
        if self.tmp_catalog and os.path.isdir(self.tmp_catalog):
            shutil.rmtree(self.tmp_catalog)


class MediaBackup(object):
    def __init__(self):
        self.create_tmp()

    def pack(self):
        media_root = getattr(settings, 'MEDIA_ROOT')
        filename = os.path.join(self.tmp_catalog, 'media')
        media = shutil.make_archive(filename, 'zip', root_dir=media_root)
        self.archive_path = media

    def create_tmp(self):
        self.tmp_catalog = tempfile.mkdtemp()

    def clean_tmp(self):
        if self.tmp_catalog and os.path.isdir(self.tmp_catalog):
            shutil.rmtree(self.tmp_catalog)
