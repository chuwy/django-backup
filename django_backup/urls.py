from django.conf.urls import patterns, url

from django_backup.views import create_backup, list_backup

urlpatterns = patterns('',
                       url(r'^create/$',
                           create_backup,
                           name='create-backup'),

                       url(r'^list/$',
                           list_backup,
                           name='list-backup'),
                       )
