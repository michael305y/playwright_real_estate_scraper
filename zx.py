import os
import django
import asyncio

import time
from playwright.sync_api import sync_playwright
from asgiref.sync import sync_to_async

from playwright.async_api import async_playwright

from asgiref.sync import sync_to_async
# from django.core.management.base import BaseCommand
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_scraper_project.settings")
django.setup()

from real_estate_scraper_app.models import Agent_profile_details

print(len(Agent_profile_details.objects.all()))

# def get_total():
#         total = Agent_profile_details.objects.all()
#         return total

# async def save_to_DB():
#         total = await sync_to_async(get_total)
#         return total

# async def save_to_DB():
#     # Wrap the callable and execute it asynchronously
#     total = await sync_to_async(Agent_profile_details.objects.count())
#     return total

async def check_DB():
    # Get the total count of objects in the database
    # total_count = await sync_to_async(Agent_profile_details.objects.count())
    total_count = await sync_to_async(Agent_profile_details.objects.count)()
    print(f"Total objects in Agent_profile_details: {total_count}")
    return total_count
        

async def main():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                BASE_URL = 'http://127.0.0.1:8000/'


                await page.goto(BASE_URL)

                # await print(len(Agent_profile_details.object
                total = await check_DB()
                # print(total)

                print(await page.title())
                await browser.close()

asyncio.run(main())