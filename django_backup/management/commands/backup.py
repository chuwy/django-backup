from datetime import datetime
from datetime import timedelta
from optparse import make_option
import os
import re
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from django_backup.utils import import_class


class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"
    option_list = BaseCommand.option_list + (
        make_option('--email',
                    default=None,
                    dest='email',
                    help="Sends email with attached dump file"),)


    def __init__(self, *args, **kwargs):
        """
        Load savers and backupers, set command options based on them.
        """
        super(Command, self).__init__(*args, **kwargs)
        default_config = [
            {'saver': 'django_backup.savers.LocaldirSaver',
             'backups': ['django_backup.backups.MediaBackup']}
        ]
        backup_config = getattr(settings, 'BACKUP_CONFIG', default_config)
        self.savers = []
        for backup_saver in backup_config:
            SaverClass = import_class(backup_saver['saver'])
            saver = SaverClass()
            self.savers.append(saver)
            for backup in backup_saver['backups']:
                BackupClass = import_class(backup)
                saver.append_backup(BackupClass)


    def handle(self, *args, **options):
        for saver in self.savers:
            saver.save()
