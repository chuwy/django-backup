from django.conf import settings
from django.shortcuts import render_to_response

from django_backup.utils import import_class


def create_backup(request):
    default_config = [
        {'saver': 'django_backup.savers.LocaldirSaver',
         'backupers': ['django_backup.backupers.MediaBackuper']}
    ]
    backup_config = getattr(settings, 'BACKUP_CONFIG', default_config)
    savers = []
    for backup_saver in backup_config:
        SaverClass = import_class(backup_saver['saver'])
        saver = SaverClass()
        savers.append(saver)
        for backuper in backup_saver['backupers']:
            BackuperClass = import_class(backuper)
            saver.append_backuper(BackuperClass)

    for saver in savers:
        saver.prepare()
        saver.save()
        saver.close_archive()
    return render_to_response('django_backup/backup_create.html')


def list_backup(request):
    default_config = [
        {'saver': 'django_backup.savers.LocaldirSaver',
         'backupers': ['django_backup.backupers.MediaBackuper']}
    ]
    backup_config = getattr(settings, 'BACKUP_CONFIG', default_config)
    savers = list()
    context = {'savers': []}
    for backup_saver in backup_config:
        SaverClass = import_class(backup_saver['saver'])
        saver = SaverClass()
        savers.append(saver)

    for saver in savers:
        context['savers'].append(saver)
    return render_to_response('django_backup/backup_list.html', context)
