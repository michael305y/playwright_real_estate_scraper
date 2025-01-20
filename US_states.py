from collections import deque
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


def grab_state_names(page, BASE_URL):
            """
            grabs all the 50 states in the US by navigating to each and every URL instead of using the next button
            """

            STARTING_URL = 'https://www.coldwellbanker.com'
            
            #   /sitemap/agents/kentucky-real-estate-agents      # the partial URL to join to the starting URL

            STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/{state}-real-estate-agents'

            STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/alabama-real-estate-agents'

            page.goto(BASE_URL)

            state_names_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all()
            state_name = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all_text_contents()
            
            state_urls_deque = deque()

            for state_locator in state_names_locators[1:]:
                partial_state_url = state_locator.get_attribute('href')
                # print(partial_state_url)

                full_state_url = STARTING_URL + partial_state_url
                print(full_state_url)

                state_urls_deque.append(full_state_url)

            print(f" Found {len(state_urls_deque)} states")
            return state_urls_deque