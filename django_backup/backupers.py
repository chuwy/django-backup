#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import tempfile
from zipfile import ZipFile

from django.conf import settings


class BaseBackuper(object):
    def __init__(self, path=None):
        if not path:            # Creating (not restoring) backup
            self.create_tmp()
        else:
            self.path = path

    def create_tmp(self):
        self.tmp_catalog = tempfile.mkdtemp()

    def clean_tmp(self):
        if self.tmp_catalog and os.path.isdir(self.tmp_catalog):
            shutil.rmtree(self.tmp_catalog)

    def get_path(self):
        return os.path.join(self.tmp_catalog, self.get_filename())

    @classmethod
    def get_filename(cls):
        """ Return FULL filename (with extension). """
        suffix = cls.get_extension()
        filename = getattr(cls, 'filename')
        if suffix:
            return filename + '.' + suffix
        else:
            return filename

    @classmethod
    def get_extension(cls):
        extension = getattr(cls, 'extension')
        if not extension:
            extension = ''
        return extension


class PostgresBackuper(BaseBackuper):
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
        if db.get('HOST'): command += ' -h {HOST}'.format(db['HOST'])
        if db.get('PORT'): command += ' -p {PORT}'.format(db['PORT'])
        os.environ['PGPASSWORD'] = db['PASSWORD']
        subprocess.Popen(command.split()).wait()
        self.db = filename

    def unpack(self):
        db = getattr(settings, 'DATABASES')['default']
        command_tmpl = 'pg_restore -i -U {USER} -d {NAME} -v {FILE}'
        command = command_tmpl.format(
            USER=db['USER'],
            NAME=db['NAME'],
            FILE=self.path)
        if db.get('HOST'): command += ' -h {HOST}'.format(db['HOST'])
        if db.get('PORT'): command += ' -p {PORT}'.format(db['PORT'])
        os.environ['PGPASSWORD'] = db['PASSWORD']
        subprocess.Popen(command.split()).wait()


class MediaBackuper(BaseBackuper):
    filename = 'media'
    extension = 'zip'

    def pack(self):
        media_root = getattr(settings, 'MEDIA_ROOT')
        filename = os.path.join(self.tmp_catalog, self.filename)
        media = shutil.make_archive(filename,
                                    self.get_extension(),
                                    root_dir=media_root)
        self.archive_path = media

    def unpack(self):
        media_root = getattr(settings, 'MEDIA_ROOT')
        archive = ZipFile(self.path, 'r')
        archive.extractall(path=media_root)
        archive.close()

class RequirementsBackuper(BaseBackuper):
    pass
