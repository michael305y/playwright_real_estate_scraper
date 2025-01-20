from asyncio import sleep
from django.utils import timezone
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://playwright.dev")
            print(page.title())
            print(page.title())
            print(page.title())
            browser.close()
                

