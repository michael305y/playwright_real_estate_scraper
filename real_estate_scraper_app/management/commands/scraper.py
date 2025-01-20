from asyncio import sleep
from django.utils import timezone
from django.core.management.base import BaseCommand

from real_estate_scraper_app.models import Agent_profile_details

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # while True:
        try:
            while True:
                time = timezone.now().strftime('%X')
                self.stdout.write(f"It's now {time}")
                
                # Example of inserting data for testing
                # Uncomment the following line if needed
                # Agent_profile_details.objects.create(agent_name='example_name')

                # Print the current record count
                record_count = Agent_profile_details.objects.count()
                self.stdout.write(f"Current record count: {record_count}")

                sleep(6)
        except KeyboardInterrupt:
            self.stdout.write("Command interrupted. Exiting gracefully.")