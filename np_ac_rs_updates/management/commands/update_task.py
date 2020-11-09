""""
Ovo je komanda koja ce periodicno da se izvrsava i da azurira bazu podataka
Kako i zasto je sve ovo ovako pise u dokumentaciji:
https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
Mora da se nalazi u .../management/commands
i poziva se sa: python manage.py update_task
"""
from django.core.management.base import BaseCommand, CommandError
from np_ac_rs_updates.popuni_bazu import popuni_bazu
from np_ac_rs_updates.send_notifications import send_notification_filter, send_notification_test

class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        popuni_bazu()