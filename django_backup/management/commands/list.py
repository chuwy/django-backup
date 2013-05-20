from django.conf import settings
from django.core.management.base import BaseCommand

from django_backup.utils import import_class


class Command(BaseCommand):
    help = "List all available backups"

    def __init__(self, *args, **kwargs):
        """
        Load savers and backupers, set command options based on them.
        """
        super(Command, self).__init__(*args, **kwargs)
        default_config = [
            {'saver': 'django_backup.savers.LocaldirSaver',
             'backupers': ['django_backup.backupers.MediaBackuper']}
        ]
        backup_config = getattr(settings, 'BACKUP_CONFIG', default_config)
        self.savers = []
        for backup_saver in backup_config:
            SaverClass = import_class(backup_saver['saver'])
            saver = SaverClass()
            self.savers.append(saver)

    def handle(self, *args, **options):
        for saver in self.savers:
            self.stdout.write('Backups in %s:\n' % saver)
            for backup in saver.list():
                print backup

