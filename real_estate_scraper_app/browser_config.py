import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # browser = p.chromium.launch()  # 1. headless option

    browser = p.chromium.launch(headless=False)  # 2. headed mode

    page = browser.new_page()

    try:
        # if it headless then enable
        # if headless mode:  # uncomment the below hhtp headers
        # page.set_extra_http_headers({
        #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        #  })

        pass
    except Exception as e:
        print(e)    

    # if headless mode:  # uncomment the below hhtp headers
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    BASE_URL = 'https://www.coldwellbanker.com/city/al/abbeville/agents'
    # BASE_URL = 'https://www.coldwellbanker.com/city/al/hazel-green/agents'

    # BASE_URL = 'https://www.coldwellbanker.com'
    # BASE_URL = 'http://playwright.dev'
    # BASE_URL = "https://example.com"

    # page.goto("https://example.com")
    page.goto(BASE_URL)