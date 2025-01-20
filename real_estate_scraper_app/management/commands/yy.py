
import os
import django
import asyncio

import time
from playwright.sync_api import sync_playwright
from asgiref.sync import sync_to_async

from playwright.async_api import async_playwright

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone

from asgiref.sync import async_to_sync
from real_estate_scraper_app.models import Agent_profile_details

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # Wrap the asynchronous main function with async_to_sync
        async_to_sync(self.main)()

    async def fetch_agent_count(self):
        """Fetch the count of agent profile details from the database."""
        # Wrap ORM call with sync_to_async
        count = await sync_to_async(Agent_profile_details.objects.count)()
        return count

    async def main(self):
        async with async_playwright() as p:
            # Launch the browser in headed mode
            browser = await p.chromium.launch(headless=False)

            # Open a new page
            page = await browser.new_page()

            # Set HTTP headers for the page
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

            # Define the base URL
            BASE_URL = 'http://127.0.0.1:8000/'

            # Navigate to the base URL
            await page.goto(BASE_URL)

            # Simulate a delay
            await asyncio.sleep(2)

            await sync_to_async(Agent_profile_details.objects.count)()

            # Fetch agent count from the database
            try:
                agent_count = await self.fetch_agent_count()
                print(f"Number of Agent Profile Details: {agent_count}")
            except Exception as e:
                print(f"Error fetching agent count: {e}")
    
            title = await page.title()
            print(title)

            # Close the browser
            # await browser.close()
