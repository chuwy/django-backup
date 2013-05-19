from datetime import datetime
import os
import zipfile

from django.conf import settings


class BaseSaver(object):
    """
    Just an interface
    """
    def get_path(self):
        raise NotImplementedError

    def save(self, backup=None):
        raise NotImplementedError

    def get_last(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError


class RsyncSaver(object):
    pass


class LocaldirSaver(object):
    """
    Class responsible for manipulating with completed packed backups
    stored in local directory.
    """

    def __init__(self):
        self.path = getattr(settings, 'BACKUP_SAVER_LOCALDIR')
        self.backups = []

    def get_path(self):
        pass

    def get_archive(self):
        now = datetime.today().strftime('%d-%m-%Y_%H-%M')
        filename = os.path.join(self.path, now + '.zip')
        self.archive = zipfile.ZipFile(filename, 'w')

    def save(self):
        for Backuper in self.backups:
            backup = Backuper()
            backup.pack()
            self.archive.write(backup.get_path())

    def list(self):
        return os.listdir(self.path)

    def get_last(self):
        all_backups = self.list()
        all_backups.sort(
            key=lambda x: datetime.strptime(x, '%d-%m-%Y_%H-%M.zip'))
        return all_backups[-1]

    def restore(self, backup=None):
        pass

    def append_backup(self, backup):
        self.backups.append(backup)

    def close_archive(self):
        self.archive.close()


class EmailSaver(object):
    pass


class GlacierSaver(object):
    pass


class SCPSaver(object):
    pass


class FTPSaver(object):
    pass
