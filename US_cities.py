"""
========= grab and retrieve all the cities in the specified state
"""

from collections import deque
from time import sleep
from playwright._impl._errors import TimeoutError as PlayWrightTimeoutError

from real_estate_crawler_app.styling_colors import BLUE_COLOR, GREEN_COLOR, RESET_COLOR


def grab_cities_by_their_urls(page, state_urls):
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

    while state_urls:
            current_url =   state_urls.popleft()
            print(f"current url: {GREEN_COLOR} {current_url} {RESET_COLOR}")

            # page.goto(current_url)
            page.goto(current_url, timeout=20000)
            print(f"{BLUE_COLOR} {page.title()} {RESET_COLOR}")

            print(' searching for cities...')
            sleep(2)

        # ====================== actual locator ==================================
                                # MuiTypography-root.MuiTypography-inherit MuiLink-root.MuiLink-underlineHover
            city_locators = page.locator('a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover').all()
            # name_of_cities = page.locator('p.MuiTypography-root.MuiTypography-body1.css-1vn50qe').all_text_contents()

            print(f" {len(city_locators[2:])} cities ")
            
            cities_urls_deque = deque()

            STARTING_URL = 'https://www.coldwellbanker.com'

            for city_locator in city_locators[2:]:
                partial_city_url = city_locator.get_attribute('href', timeout=10000)  # we are only getting the partial URL
                # partial_city_url_text= city_locator.text_content() # for testing
                print(partial_city_url)

                full_city_url = STARTING_URL + partial_city_url
                print(full_city_url)  # for testing to show that we are in that city

                cities_urls_deque.append(full_city_url)
        
        
            
            print(f" {BLUE_COLOR } navigating to each city... {RESET_COLOR}")

            
            
            #============ for each city start grabbing agent details ==================

    #     #  while cities_urls_deque:
    #     #     current_url =   cities_urls_deque.popleft()
    #     #     print(f"current url: {GREEN_COLOR} {current_url} {RESET_COLOR}")
    #     #     page.goto(current_url)
    #     #     sleep(3)

    #     #     try:
    #     #         office_name_locator = page.get_by_test_id('office-name')   # grabs the name of an agent
    #     #         no_agents_found = page.get_by_text("No agents found", exact=True)
    #     #         # page.wait_for_load_state()

    #     #         if no_agents_found.is_visible():
    #     #             print('no agents found')
    #     #             page.go_back()
    #     #             return
    #     #         else:

    #     #             page.wait_for_selector('[data-testid="office-name"]')  # wait for name to be visible
    #     #             # page.wait_for_selector('[data-testid="emailLink"]', timeout=20000)  # wait for email to be visible

    #     #             print(page.url)

    #     #             # name_elements_2 = page.locator('[data-testid="office-name"]') 
    #     #             name_elements = page.get_by_test_id("office-name")
    #     #             print(name_elements.all_text_contents())
    #     #             name_text = name_elements.all_text_contents()

    #     #             print(f" {GREEN_COLOR} Found  {len(name_text)} agents {RESET_COLOR}")
                    
    #     #             # for name in name_text:
    #     #             #     print(name)
                        
    #     #                 # names_deque.append(name)
                    
    #     #             # return names_deque
                
    #     #             phone_numbers = page.get_by_test_id('phoneNumber').all_text_contents()
    #     #             # print(phone_number)
                    
    #     #             # for phone in phone_numbers:
    #     #             #     print(phone)

    #     #             for name, phone in zip(name_text, phone_numbers):
    #     #                 print(f" {name} - {phone}")

    #     # #             # emails = page.get_by_test_id('emailDiv')  #1
    #     # #             emails = page.get_by_test_id('emailLink').all()  #2

    #     # #             # page.wait_for_selector()
    #     # #             print(len(emails))
    #     # #             # print(emails)

    #     # #             for email in emails:
    #     # #                 print(email.get_attribute('href'))

    #     #         # async  save_to_DB()
    #     #                 # await sync_to_async(save_to_DB())

    #     #     except PlayWrightTimeoutError as e:
    #     #         print(f"cannot find office name locator {e}")

    # print('done processing')
    return cities_urls_deque
    