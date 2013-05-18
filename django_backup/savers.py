import os

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

    def save(self, backup=None):
        for Backuper in self.backups:
            backup = Backuper()
            backup.pack()

    def list(self):
        return os.listdir(self.path)

    def get_last(self):
        pass

    def restore(self, backup=None):
        pass

    def append_backup(self, backup):
        self.backups.append(backup)

class EmailSaver(object):
    pass


class GlacierSaver(object):
    pass


class SCPSaver(object):
    pass


class FTPSaver(object):
    pass
