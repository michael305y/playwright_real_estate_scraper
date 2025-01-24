"""
scraper cmmand imports from the main_scraper module
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import asyncio
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_scraper_project.settings")
django.setup()

from asgiref.sync import sync_to_async

from real_estate_scraper_app.models import Agent_profile_details, all_states_links, cities_real_estate_links

from real_estate_scraper_app.styling_colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, RESET_COLOR


from main_scraper import main


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # while True:
        try:
            time = timezone.now().strftime('%X')
            self.stdout.write(f"It's now {time}")

            asyncio.run(main())
                

            # sleep(6)
        except KeyboardInterrupt:
            self.stdout.write("Command interrupted... Exiting...")