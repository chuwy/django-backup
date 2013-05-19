import os
from optparse import make_option
from tempfile import gettempdir
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Restores choosen backup"

    def handle(self, *args, **options):
        pass
