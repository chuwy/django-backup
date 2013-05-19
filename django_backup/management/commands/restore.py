import os
from optparse import make_option
from tempfile import gettempdir
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Restores latest backup."
    option_list = BaseCommand.option_list + (
        make_option('--media', '-m',
                    action='store_true',
                    dest='media',
                    help='Restore media dir'),)

    def handle(self, *args, **options):
        pass
