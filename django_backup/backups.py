#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import tempfile

from django.conf import settings


class BaseBackuper(object):
    def __init__(self):
        self.create_tmp()

    def create_tmp(self):
        self.tmp_catalog = tempfile.mkdtemp()

    def create_tmp_file(self, extension):
        if extension:
            extension = '.' + extension
        return tempfile.mkstemp(suffix=extension)[1]

    def clean_tmp(self):
        if self.tmp_catalog and os.path.isdir(self.tmp_catalog):
            shutil.rmtree(self.tmp_catalog)

    def get_path(self):
        return os.path.join(self.tmp_catalog, self.get_filename())

    def get_filename(self):
        """
        Return FULL filename (with extension).
        """
        suffix = self.get_extension()
        filename = getattr(self, 'filename')
        if not filename:
            filename = self.create_tmp_file(suffix)
            return filename
        else:
            if suffix:
                return filename + '.' + suffix
            else:
                return filename

    def get_extension(self):
        extension = getattr(self, 'extension')
        if not extension:
            extension = ''
        return extension


class PostgresBackup(BaseBackuper):
    filename = 'db'
    extension = 'sql'

    def pack(self):
        db = getattr(settings, 'DATABASES')['default']
        filename = os.path.join(self.tmp_catalog, self.get_filename())
        command_tmpl = 'pg_dump -o -w -Fc -Z 7 -U {USER} -C -f {FILE} {NAME}'
        command = command_tmpl.format(
            USER=db['USER'],
            NAME=db['NAME'],
            FILE=filename)
        subprocess.Popen(command.split()).wait()
        self.db = filename


class MediaBackup(BaseBackuper):
    filename = 'media'
    extension = 'zip'

    def pack(self):
        media_root = getattr(settings, 'MEDIA_ROOT')
        filename = os.path.join(self.tmp_catalog, self.filename)
        media = shutil.make_archive(filename,
                                    self.get_extension(),
                                    root_dir=media_root)
        self.archive_path = media
