from datetime import datetime
import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

from django.conf import settings


class BaseSaver(object):
    backupers = list()
    settings = dict()

    def append_backuper(self, backuper):
        self.backupers.append(backuper)

    def parse_settings(self):
        """
        Get from settings.py every settings which starts with
        uppercase classname and save it to self.settings dict.
        """
        class_name = self.__class__.__name__.upper()
        for setting_name in dir(settings):            # Django-project settings
            if setting_name.startswith('BACKUP_' + class_name + '_'):
                setting = getattr(settings, setting_name)
                self.settings.update(
                    {setting_name[8 + len(class_name):].lower(): setting}
                )


class LocaldirSaver(BaseSaver):
    """
    Class responsible for manipulating with completed packed backups
    stored in local directory.
    """

    def __init__(self):
        """ Set all settings """
        self.parse_settings()
        self.path = self.settings.get('dir')
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.isdir(self.path):
            raise IOError("BACKUP_LOCALDIRSAVER_DIR ({})"
                          "is not a directory".format(self.path))

    def prepare(self):
        """ Create archive """
        now = datetime.today().strftime('%d-%m-%Y_%H-%M')
        filename = os.path.join(self.path, now + '.zip')
        self.archive = ZipFile(filename, 'w')

    def save(self):
        """
        Call each backuper's pack() and add it's content (from backup.get_path()
        to saver's archive.
        """
        for Backuper in self.backupers:
            backup = Backuper()
            backup.pack()
            self.archive.write(backup.get_path(),
                               backup.get_path().split(os.sep)[-1],
                               ZIP_DEFLATED)

    def list(self):
        """ List all backups. Should return list of filenames """
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

    def close_archive(self):
        self.archive.close()


class SCPSaver(BaseSaver):
    pass


class RsyncSaver(BaseSaver):
    pass


class GlacierSaver(BaseSaver):
    pass


class FTPSaver(BaseSaver):
    pass


class EmailSaver(BaseSaver):
    pass
