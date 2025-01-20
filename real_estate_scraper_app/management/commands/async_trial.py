from itertools import zip_longest
from time import sleep
import django
import os
import asyncio
from collections import deque
from playwright.async_api import async_playwright
from asgiref.sync import sync_to_async

from django.core.management.base import BaseCommand
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_scraper_project.settings")
django.setup()

from real_estate_scraper_app.models import Agent_profile_details, all_states_links, cities_real_estate_links

from real_estate_scraper_app.styling_colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, RESET_COLOR



class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)
        async def grab_state_names(page, BASE_URL):
                    """
                    grabs all the 50 states in the US by navigating to each and every URL instead of using the next button
                    """

                    STARTING_URL = 'https://www.coldwellbanker.com'
                    
                    #   /sitemap/agents/kentucky-real-estate-agents      # the partial URL to join to the starting URL

                    STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/{state}-real-estate-agents'
                    STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/alabama-real-estate-agents'

                    await page.goto(BASE_URL)

                    state_names_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover')
                    # state_name = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all_text_contents()
                    
                    state_names_link_locators = await state_names_locators.all()

                    state_names_deque = deque()
                    state_urls_deque = deque()

                    print(f"Found {len(state_names_link_locators)} state links (including heading):")

                    for state_locator in state_names_link_locators[1:]:
                        partial_state_url = await state_locator.get_attribute('href')
                        state_name = await state_locator.text_content()
                        # print(partial_state_url)
                        # print(state_name)
                        # print(f"{state_name}  ->   {partial_state_url}")

                        full_state_url = STARTING_URL + partial_state_url
                        # print(full_state_url)   # for testing

                        state_names_deque.append(state_name)
                        state_urls_deque.append(full_state_url)

                    await save_statenames_to_DB(state_names_deque, state_urls_deque)

                    print(await page.title())  ## for testing purpose
                        
                    # print(f" Found {len(state_urls_deque)} states")
                    return state_urls_deque


        # ========================== cities logic ============================================

        async def grab_cities_by_their_urls(page, state_urls):
            """
            returns a list of URLS of all cities in  the selected(current state) state.
            this method avoids clciking the nNEXT PAGE button
            """

            STARTING_URL = 'https://www.coldwellbanker.com'

            # STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/{state}-real-estate-agents'
            # STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/alabama-real-estate-agents'
            
            #   "/city/ma/south-hadley/agents"    # the partial URL to join to the starting URL

            # CITY_BASE_URL =  'https://www.coldwellbanker.com/city/ma/cambridge/agents'

            # page.goto(STATE_BASE_URL)   # for testin
            
            # while state_urls:
            while len(state_urls) > 49:  # for testing
                    current_url =   state_urls.popleft()
                    # current_url =   state_urls.pop()
                    print(f"current url: {GREEN_COLOR} {current_url} {RESET_COLOR}")

                    # page.goto(current_url)
                    await page.goto(current_url, timeout=20000)
                    title = await page.title()

                    # incase of 502 error
                    if title ==  "502 Bad Gateway":
                        #   return
                        pass

                    print(f"{BLUE_COLOR} {title} {RESET_COLOR}")

                    current_state = title.split('-')[0].replace(' Real Estate Agents', " ")

                    print(f" searching for cities in {GREEN_COLOR} {current_state} {RESET_COLOR}")
                    await asyncio.sleep(2)

                # ====================== actual locator ==================================
                                        # MuiTypography-root.MuiTypography-inherit MuiLink-root.MuiLink-underlineHover
                    city_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover')
                    # name_of_cities = page.locator('p.MuiTypography-root.MuiTypography-body1.css-1vn50qe').all_text_contents()
                    all_city_locators = await city_locators.all()

                    print(f" {len(all_city_locators[2:])} cities ")
                    
                    cities_urls_deque = deque()
                    city_names_deque = deque()

                    STARTING_URL = 'https://www.coldwellbanker.com'


                    # for city_locator in all_city_locators[2:]:   # default start is at 2 to skip heading
                    for city_locator in all_city_locators[2:5]:   # default start is at 2 to skip heading
                        partial_city_url = await city_locator.get_attribute('href', timeout=10000)  # we are only getting the partial URL
                        full_city_url = STARTING_URL + partial_city_url

                        city_name = await city_locator.text_content() # for testing
                        # print(city_name)

                        # print(f" {city_name} ->  {full_city_url}")

                    #     # asynchronlusly gather the cities
                    #     # asyncio.current_task()

                        cities_urls_deque.append(full_city_url)
                        city_names_deque.append(city_name)

                    await save_cities_to_DB(city_names_deque, cities_urls_deque)

                    # return cities_urls_deque
                
                    print(f" {BLUE_COLOR }I'm starting to navigate to each city... {RESET_COLOR}")


                            
                    #============ for each city start grabbing agent details ==================
                    # cities = await get_city_urls_from_DB()
                    # # print(cities)
                


                    # while cities_urls_deque:
                    #         current_url =   cities_urls_deque.popleft()
                    #         print(f"current city url: {GREEN_COLOR} {current_url} {RESET_COLOR}")
                    #         # page.goto(current_url)
                    #         await asyncio.sleep(3)  
        # ========================== end of cities logic ============================================

        async def grab_agent_profile_details(page, city_urls):
            """
            Grabs the profile details of each agent:
            1. Name
            2. Phone number
            3. Email
            """
            while city_urls:
                current_url = city_urls.popleft()
                print(f"Current city URL: {GREEN_COLOR} {current_url} {RESET_COLOR}")
                await page.goto(current_url)

                code, c = current_url.replace('https://www.coldwellbanker.com/city/', '').split('/')[:2]
                state_code = code.upper()
                city = c.replace('-', ' ').title()

                print(f"I'm currently in {state_code, city}")

                agent_names_list = []
                agent_phoneNumbers_list = []
                agent_emails_list = []
                agent_license_No_list = []

                while True:  # Loop to handle pagination
                    await asyncio.sleep(3)  # Allow page content to load

                    # Extract agent details
                    agent_name_locator = page.get_by_test_id("office-name")
                    agent_names = await agent_name_locator.all_text_contents()

                    phone_number_locator = page.get_by_test_id('phoneNumber')
                    agent_phone_numbers = await phone_number_locator.all_text_contents()

                    license_number_locator = page.get_by_test_id('license-number')
                    agent_license_numbers = await license_number_locator.all_text_contents()

                    email_locator = page.get_by_test_id('emailLink')
                    all_emails_locator = await email_locator.all()

                    processed_emails = []
                    for mail in all_emails_locator:
                        email = await mail.get_attribute('href')
                        processed_email = email.replace('mailto:', "").strip()
                        processed_emails.append(processed_email)

                    if not agent_names:
                        print(f"{GREEN_COLOR}No agents found on this page{RESET_COLOR}")
                    else:
                        # for agent_name, agent_phone_number, agent_email, license_number in zip(agent_names, agent_phone_numbers, processed_emails, agent_license_numbers):
                        for agent_name, agent_phone_number, agent_email, agent_license_number in zip_longest(agent_names, 
                                                                                                    agent_phone_numbers,
                                                                                                    processed_emails, 
                                                                                                    agent_license_numbers, 
                                                                                                    fillvalue=None):
                        
                            print(f"{agent_name} --> {agent_phone_number} - {agent_email} - {agent_license_number}")
                            # print(city, state_code)
                        
                            agent_names_list.append(agent_name)
                            agent_phoneNumbers_list.append(agent_phone_number)
                            agent_emails_list.append(agent_email)
                            agent_license_No_list.append(agent_license_number)

                    # ===== Logic for Next Page button ================================================
                    try:
                        next_page_button = page.get_by_test_id("NavigateNextIcon") 
                        if await next_page_button.is_visible() and not await next_page_button.is_disabled():
                            print(f"{BLUE_COLOR}Navigating to the next page...{RESET_COLOR}")
                            await next_page_button.hover()
                            await next_page_button.click()
                            # await page.wait_for_load_state('networkidle')  # Wait for the next page to load

                            print(f" Found {len(agent_names_list)} agents so far")
                        else:
                            print(f"{RED_COLOR}No more pages to navigate{RESET_COLOR}")

                            await save_agent_to_DB(agent_names_list, agent_phoneNumbers_list, agent_emails_list, agent_license_No_list)

                            break
                    except Exception as e:
                        print(f"{RED_COLOR}Error with Next Page button: {e}{RESET_COLOR}")
                        break
                    # ===== End of Logic for Next Page button ================================================




        async def save_agent_to_DB(agent_names_list, agent_phoneNumbers_list, agent_emails_list, agent_license_No_list):
            '''
            saves agent profile details to DB
            '''
            #   await sync_to_async(Agent_profile_details.objects.create)(agent_name=agent_name)
            agents_object = [ Agent_profile_details(agent_name=agent_name, 
                                                    agent_phone=agent_phone, 
                                                    agent_email=agent_email,
                                                    agent_license_number=agent_license_number )  # "No License Found"
                            for agent_name, agent_phone, agent_email, agent_license_number in zip(agent_names_list, 
                                                                            agent_phoneNumbers_list, 
                                                                            agent_emails_list,
                                                                            agent_license_No_list)]


            # agents_phone_object = [ Agent_profile_details(agent_name=agent_phone) for agent_phone in agent_phoneNumbers_list]
            print('saving agent profile to DB')

            await sync_to_async(Agent_profile_details.objects.bulk_create)(agents_object)

            total_No_of_all_agents = await sync_to_async(Agent_profile_details.objects.count)()
            print(total_No_of_all_agents)



        async def save_statenames_to_DB(state_names_deque, state_urls_deque):
            total_no_of_states =  await sync_to_async(all_states_links.objects.count)()
            if total_no_of_states == 51:
                    print('all states exist')
                    return
            else:
                while state_urls_deque and state_urls_deque:
                        state_name = state_names_deque.popleft() or "Unknown state"
                        state_url = state_urls_deque.popleft() or "Unknown URL"
                        print(f" {state_name} ->  {state_url}")
                        
                        await sync_to_async(all_states_links.objects.create)(state_name=state_name, Link_to_real_estate=state_url)

                print('Saved all state names')
                    
            total_no_of_states =  await sync_to_async(all_states_links.objects.count)()
            print(f" Found {total_no_of_states} states")
            #   return total_no_of_states


        async def get_state_urls_from_DB():
            """
            returns the list of all state URLs from the DB
            """
            #   state_urls = await sync_to_async(list(all_states_links.objects.values_list))('Link_to_real_estate')
            state_urls = await sync_to_async(list)(all_states_links.objects.values_list('Link_to_real_estate', flat=True))
            #   print(state_urls)

            #   return state_urls    ##  as a list
            return deque(state_urls)  # as a deque

        
        async def save_cities_to_DB(city_names_deque, cities_urls_deque):
            """
            saves citiy names and their URLs to the DB
            """
            all_city_urls = await sync_to_async(list)(cities_real_estate_links.objects.values_list('link_to_city', flat=True))
            total_no_of_cities =  await sync_to_async(cities_real_estate_links.objects.count)()
            if total_no_of_cities == 51:
                pass
            else:
                while city_names_deque and cities_urls_deque:
                        city_name = city_names_deque.popleft() or "Unknown city"
                        city_url = cities_urls_deque.popleft() or "Unknown city URL"

                        if city_url in  all_city_urls:
                            print('city already exists')
                            continue
                        
                        await sync_to_async(cities_real_estate_links.objects.create)(city_name=city_name, link_to_city=city_url)
                        print(f" Saving {city_name} ->  {city_url}")

                print('Done processing')
                    
            total_no_of_cities =  await sync_to_async(cities_real_estate_links.objects.count)()
            print(f" Found {total_no_of_cities} cities")
            #   return total_no_of_states


        async def get_city_urls_from_DB():
            """
            returns the list of all city URLs from the DB
            """
            
            city_urls = await sync_to_async(list)(cities_real_estate_links.objects.values_list('link_to_city', flat=True))
            #   print(state_urls)

            #   return state_urls    ##  as a list
            return deque(city_urls)  # as a 



        async def main():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)   # remember if you set headless to true then enable(uncomment) the http headers below
                page = await browser.new_page()

                # ============ optional browser configurations==========================
                await page.set_extra_http_headers({
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    })

                # await page.route("**/*.{jpg, png, jpeg}", lambda route: route.abort())

                
                # ================ end of browser configurations =============================

                
                BASE_URL = 'https://www.coldwellbanker.com/sitemap/agents'

                # await page.goto("http://127.0.0.1:8000/agents'")
                await page.goto(BASE_URL, timeout=60000)  
                print(await page.title())

                await grab_state_names(page, BASE_URL)
                # state_urls = await grab_state_names(page, BASE_URL)   ## ets state URLs from dynamic locating

                state_urls = await get_state_urls_from_DB()  ## gets URLs from  States DB

                if not state_urls:
                    print("No state URLS found")
                    return
                # for url in state_urls:
                #       print(url)

                await grab_cities_by_their_urls(page, state_urls)

                city_urls = await get_city_urls_from_DB()    # get URLs of each city to use grab profile details
                # print(city_urls)

                if not city_urls:
                    print('No cities found')
                    return
                else:
                    await grab_agent_profile_details(page, city_urls)
                    #   await next_page(page, city_urls)

                    


                await browser.close()

        asyncio.run(main())