from django.core.management.base import BaseCommand, CommandError
from django.db import *

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        pass