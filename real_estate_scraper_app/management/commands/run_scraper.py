"""
custom command to display current time and adding movies to the DB
"""

from collections import deque
from time import sleep

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils import timezone
from playwright._impl._errors import TimeoutError as PlayWrightTimeoutError
from playwright.sync_api import sync_playwright


from real_estate_scraper_app.models import Agent_profile_details
from real_estate_scraper_app.styling_colors import (BLUE_COLOR, GREEN_COLOR,  RED_COLOR, RESET_COLOR)

# from profile_details_of_agents import next_page, grab_profile_details


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)




        BASE_URL = 'https://www.coldwellbanker.com/sitemap/agents'

        def grab_state_names():
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

            print(len(state_urls_deque))
            return state_urls_deque

        #     # print(len(state_name) - 1)

        #     # for state in state_name[1:]:                       # removing the heading
        #     #     print(state.replace('Real Estate Agents', " ")) # to grab only the state names

        #     # for state in list_of_states:
        #     #     CURRENT_STATE_URL = STATE_BASE_URL.format(state=state)

        #     #     page.goto(CURRENT_STATE_URL)
        #     #     page.goto(CURRENT_STATE_URL)
        #     #     sleep(2)

        #         # # we navigate to a city by calling the grab_city names()
        #         # grabbing_all_cities_in_each_state()

        #         # page.go_back()


        def grab_cities_by_their_urls():
            """
            returns a list of URLS of all cities in  the selected(current state) state.
            this method avoids clciking the nNEXT PAGE button
            """

            STARTING_URL = 'https://www.coldwellbanker.com'

            # STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/{state}-real-estate-agents'
            STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/alabama-real-estate-agents'
            
            #   "/city/ma/south-hadley/agents"    # the partial URL to join to the starting URL

            # CITY_BASE_URL =  'https://www.coldwellbanker.com/city/ma/cambridge/agents'

            page.goto(STATE_BASE_URL)   # for testing

            # ====================== actual locator ==================================
                                # MuiTypography-root.MuiTypography-inherit MuiLink-root.MuiLink-underlineHover
            city_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all()
            # name_of_cities = page.locator('p.MuiTypography-root.MuiTypography-body1.css-1vn50qe').all_text_contents()

            print(len(city_locators[2:]))
            
            cities_urls_deque = deque()

            try:
                for city_locator in city_locators[2:]:
                    partial_city_url = city_locator.get_attribute('href', timeout=10000)
                    # partial_city_url_text= city_locator.text_content() # for testing
                    print(partial_city_url)

                    full_city_url = STARTING_URL + partial_city_url
                    # print(full_city_url)  # for testing

                    cities_urls_deque.append(full_city_url)

                print(f"found {len(cities_urls_deque)} city urls")
                return cities_urls_deque
            
            except PlayWrightTimeoutError as e:
                print(f"city locator couldn't be found {e}")


        

        def grab_profile_details():  
            """
                grabs the profile details of each agent:
                1. name
                2. phone number
                3. email
            """ 
            names_deque = deque()

            PROFILE_AGENT_URL = 'https://www.coldwellbanker.com/city/al/abbeville/agents'   # for testing

            page.goto(PROFILE_AGENT_URL)

            try:
                office_name_locator = page.get_by_test_id('office-name')   # grabs the name of an agent
                no_agents_found = page.get_by_text("No agents found", exact=True)
                # page.wait_for_load_state()

                if no_agents_found.is_visible():
                    print('no agents found')
                    page.go_back()
                    return
                else:

                    page.wait_for_selector('[data-testid="office-name"]', timeout=20000)  # wait for name to be visible
                    page.wait_for_selector('[data-testid="emailLink"]', timeout=20000)  # wait for email to be visible

                    print(page.url)

                    # name_elements_2 = page.locator('[data-testid="office-name"]') 
                    name_elements = page.get_by_test_id("office-name")
                    print(name_elements.all_text_contents())
                    name_text = name_elements.all_text_contents()

                    print(f" {GREEN_COLOR} Found  {len(name_text)} agents {RESET_COLOR}")
                    
                    for name in name_text:
                        print(name)
                        # Agent_profile_details.objects.create(agent_name=name)
                        names_deque.append(name)
                    # print(Agent_profile_details.objects.all())
                    # save_to_DB()
                    return names_deque

                
        #             phone_number = page.get_by_test_id('phoneNumber').all_text_contents()
        #             print(phone_number)

        #             # emails = page.get_by_test_id('emailDiv')  #1
        #             emails = page.get_by_test_id('emailLink').all()  #2

        #             # page.wait_for_selector()
        #             print(len(emails))
        #             # print(emails)

        #             for email in emails:
        #                 print(email.get_attribute('href'))

            except PlayWrightTimeoutError as e:
                print(f"cannot find office name locator {e}")



        def save_to_DB():
            # print(f"Inserting to DB the following..")
            # print(names_deque)

            # while names_deque:
            #         agent_name = names_deque.popleft()
            #         Agent_profile_details.objects.create(agent_name=agent_name)
            # print('Done processing')

            No_of_agents = Agent_profile_details.objects.all()
            # return len(No_of_agents)
            print(len(No_of_agents))

            # print(Agent_profile_details.objects.all())


         


        with sync_playwright() as p:
            # remember if you set headless to true then enable the http headers below
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()  

            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

            

        #     # print(browser.is_connected())  # checks if browser is connected
        #     # browser.start_tracing(page, path="trace.json")
        #     # page.goto("https://www.google.com")
        #     # browser.stop_tracing()

        #     # page.goto(bas)

        #     # grab_state_names()
        # #     # grabbing_all_cities_in_each_state()
            # grab_profile_details()

        # sleep(4)
        # save_to_DB()

        #     # ===================== NAVIGATING TO EACH STATE BY THEIR URLS ========================


            going_through_links = grab_state_names()

            cities_urls_deque = deque()

            while going_through_links:
                current_state_url =   going_through_links.popleft()
                print(f"current url: {GREEN_COLOR} {current_state_url} {RESET_COLOR}")

                page.goto(current_state_url)
                print(f"{BLUE_COLOR} {page.title()} {RESET_COLOR}")

                print('processing the number of cities...')

                # ====================== actual locator of each city ==================================
                                
                city_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all()
                # name_of_cities = page.locator('p.MuiTypography-root.MuiTypography-body1.css-1vn50qe').all_text_contents()

                print(f"{len(city_locators[2:])} cities found")
                ## =================== end of logic ==================================================

                sleep(2)

                print(f"starting to enter each city")
                sleep(2)

                STARTING_URL = 'https://www.coldwellbanker.com'

                for city_locator in city_locators[2:]:
                    partial_city_url = city_locator.get_attribute('href', timeout=10000)  # we are only getting the partial URL
                    # partial_city_url_text= city_locator.text_content() # for testing
                    print(partial_city_url)

                    full_city_url = STARTING_URL + partial_city_url
                    print(full_city_url)  # for testing to show that we are in that city

                    cities_urls_deque.append(full_city_url)
                    

                    #============ for each city start grabbing agent details ==================
                while cities_urls_deque:
                    current_url =   cities_urls_deque.popleft()
                    print(f"current url: {GREEN_COLOR} {current_url} {RESET_COLOR}")
                    page.goto(current_url)
                    sleep(3)

                    try:
                        office_name_locator = page.get_by_test_id('office-name')   # grabs the name of an agent
                        no_agents_found = page.get_by_text("No agents found", exact=True)
                        # page.wait_for_load_state()

                        if no_agents_found.is_visible():
                            print('no agents found')
                            page.go_back()
                            return
                        else:

                            page.wait_for_selector('[data-testid="office-name"]')  # wait for name to be visible
                            # page.wait_for_selector('[data-testid="emailLink"]', timeout=20000)  # wait for email to be visible

                            print(page.url)

                            # name_elements_2 = page.locator('[data-testid="office-name"]') 
                            name_elements = page.get_by_test_id("office-name")
                            print(name_elements.all_text_contents())
                            name_text = name_elements.all_text_contents()

                            print(f" {GREEN_COLOR} Found  {len(name_text)} agents {RESET_COLOR}")
                            
                            # for name in name_text:
                            #     print(name)
                                
                                # names_deque.append(name)
                            
                            # return names_deque
                           
                        
                            phone_numbers = page.get_by_test_id('phoneNumber').all_text_contents()
                            # print(phone_number)
                            
                            # for phone in phone_numbers:
                            #     print(phone)

                            for name, phone in zip(name_text, phone_numbers):
                                print(f" {name} - {phone}")

                #             # emails = page.get_by_test_id('emailDiv')  #1
                #             emails = page.get_by_test_id('emailLink').all()  #2

                #             # page.wait_for_selector()
                #             print(len(emails))
                #             # print(emails)

                #             for email in emails:
                #                 print(email.get_attribute('href'))

                        # async  save_to_DB()
                                # await sync_to_async(save_to_DB())


                    except PlayWrightTimeoutError as e:
                        print(f"cannot find office name locator {e}")




            print('done processing')
        #     # ======================  END ======================================================



        #     # ===================== NAVIGATING TO EACH CITY BY THEIR URLS ========================

        #     # going_through_city_links = grab_cities_by_their_urls()

        #     # while going_through_city_links:
        #     #     current_url =   going_through_city_links.popleft()
        #     #     print(f"current url: {GREEN_COLOR} {current_url} {RESET_COLOR}")

        #     #     # page.goto(current_url)
        #     #     page.goto(current_url, timeout=20000)
        #     #     print(f"{BLUE_COLOR} {page.title()} {RESET_COLOR}")

        #     #     print('processing cities...')
        #     #     sleep(2)

        #     # print('done processing')
        #     # ======================  END ======================================================



