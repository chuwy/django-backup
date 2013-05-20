from datetime import datetime
import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

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
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.isdir(self.path):
            raise IOError("BACKUP_SAVER_LOCALDIR ({})"
                          "is not a directory".format(self.path))
        self.backupers = []

    def get_path(self):
        pass

    def create_archive(self):
        now = datetime.today().strftime('%d-%m-%Y_%H-%M')
        filename = os.path.join(self.path, now + '.zip')
        self.archive = ZipFile(filename, 'w')

    def save(self):
        for Backuper in self.backupers:
            backup = Backuper()
            backup.pack()
            self.archive.write(backup.get_path(),
                               backup.get_path().split(os.sep)[-1],
                               ZIP_DEFLATED)

    def list(self):
        all_backups = os.listdir(self.path)
        all_backups.sort(
            key=lambda x: datetime.strptime(x, '%d-%m-%Y_%H-%M.zip')
        )
        return all_backups

    def get_last(self):
        all_backups = self.list()
        return all_backups[-1]

    def restore(self):
        tmp_catalog = tempfile.mkdtemp()
        archive = ZipFile(os.path.join(self.path, self.get_last()), 'r')
        archive.extractall(path=tmp_catalog)
        files = os.listdir(tmp_catalog)
        for filename in files:
            for Backuper in self.backupers:
                # Choose which backuper this file belongs
                if Backuper.get_filename() == filename:
                    backuper = Backuper(os.path.join(tmp_catalog, filename))
                    backuper.unpack()

    def append_backuper(self, backup):
        self.backupers.append(backup)

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
