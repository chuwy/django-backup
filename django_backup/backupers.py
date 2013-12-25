#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import logging
import tempfile
from zipfile import ZipFile

from django.conf import settings


logger_name = getattr(settings, 'BACKUP_LOGGER', __name__)
logger = logging.getLogger(logger_name)

class BaseBackuper(object):
    def __init__(self):
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
        command_tmpl = 'pg_dump --oids --no-password --format=custom ' \
                       '--compress=7 --username={USER} --create ' \
                       '--file={FILE} {NAME}'
        command = command_tmpl.format(
            USER=db['USER'],
            NAME=db['NAME'],
            FILE=filename)
        if db.get('HOST'): command += ' -h {HOST}'.format(HOST=db['HOST'])
        if db.get('PORT'): command += ' -p {PORT}'.format(PORT=db['PORT'])
        os.environ['PGPASSWORD'] = db['PASSWORD']
        pg_dump_process = subprocess.Popen(command.split(), stderr=subprocess.PIPE)
        return_code = pg_dump_process.wait()
        if return_code:
            logger.error(u"pg_dump error {}".format(return_code))
            logger.error(pg_dump_process.stderr.read())

    def unpack(self):
        db = getattr(settings, 'DATABASES')['default']
        command_tmpl = 'pg_restore --username={USER} --dbname={NAME} ' \
                       '--verbose {FILE}'
        command = command_tmpl.format(
            USER=db['USER'],
            NAME=db['NAME'],
            FILE=self.path)
        if db.get('HOST'): command += ' -h {HOST}'.format(HOST=db['HOST'])
        if db.get('PORT'): command += ' -p {PORT}'.format(PORT=db['PORT'])
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
