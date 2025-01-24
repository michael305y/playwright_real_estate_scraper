"""
This script is designed to scrape real estate agent profiles across cities in USA. 
processes each city in every state, identifying and extracting detailed profiles of real estate agents. 
It relies on the `Detailed_profile` and `DB_functions` modules for its operations.
"""

from itertools import zip_longest
import random
from time import sleep
import django
import os
import asyncio
from collections import deque
from playwright.async_api import async_playwright
from asgiref.sync import sync_to_async
from playwright._impl._errors import TimeoutError as PlayWrightTimeoutError

from django.core.management.base import BaseCommand
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_scraper_project.settings")
django.setup()

from real_estate_scraper_app.models import Agent_profile_details, all_states_links, cities_real_estate_links

from real_estate_scraper_app.styling_colors import BLUE_COLOR, GREEN_COLOR, MAGENTA_COLOR, RED_COLOR, RESET_COLOR

from Detailed_profile import process_agent_details, process_agent_details_by_click


# class Command(BaseCommand):
#     help = 'Displays current time'

#     def handle(self, *args, **kwargs):
#         # time = timezone.now().strftime('%X')
#         # self.stdout.write("It's now %s" % time)
async def grab_state_names(page, BASE_URL):
    """
    grabs all the 50 states in the US by navigating to each and every URL instead of using the next button
    """

    STARTING_URL = 'https://www.coldwellbanker.com'
    
    #   /sitemap/agents/kentucky-real-estate-agents      # the partial URL to join to the starting URL

    # STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/{state}-real-estate-agents'
    # STATE_BASE_URL =  'https://www.coldwellbanker.com/sitemap/agents/alabama-real-estate-agents'

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
        state_name = state_name.replace(' Real Estate Agents', ' ').strip()
        # print(f"{state_name}  ->   {partial_state_url}")

        full_state_url = STARTING_URL + partial_state_url
        # print(full_state_url)   # for testing

        state_names_deque.append(state_name)
        state_urls_deque.append(full_state_url)

    await save_statenames_to_DB(state_names_deque, state_urls_deque)

    print(await page.title())  ## for testing purpose
        
    # print(f" Found {len(state_urls_deque)} states")
    # return state_urls_deque


# ========================== cities logic ============================================

async def grab_city_data_from_states(page, state_urls):
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
    found_states = len(state_urls)
    print(f" Found  {found_states} states to grab data")

    # if found_states == 51:
    #      print('all states have been processed')
    #      return
    
    while state_urls:
    # while len(state_urls) > 49:  # for testing
            current_state_url =   state_urls.popleft()
            # current_state_url =   state_urls.pop()
            print(f"current url: {GREEN_COLOR} {current_state_url} {RESET_COLOR}")

             # we pause the script for a random interval
            random_delay = random.randint(3, 20)  
            print(f"lemme rest for {random_delay} seconds before restarting...")
            await asyncio.sleep(random_delay)

            await page.goto(current_state_url, timeout=20000)
            title = await page.title()

            # incase of 502 error
            if title ==  "502 Bad Gateway":
                print(f"502 error encountered for {current_state_url}. Skipping.")
                continue
                # pass

     

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

            ## ==================================================================
            for city_locator in all_city_locators[2:]:   # default start is at 2 to skip heading
            # for city_locator in all_city_locators[2:9]:   # default start is at 2 this is for testing
                partial_city_url = await city_locator.get_attribute('href', timeout=10000)  # we are only getting the partial URL
                full_city_url = STARTING_URL + partial_city_url

                city_name = await city_locator.text_content() 

                # print(f" {city_name} ->  {full_city_url}")

            #     # asynchronlusly gather the cities
            #     # asyncio.current_task()

                cities_urls_deque.append(full_city_url)
                city_names_deque.append(city_name)

            await save_cities_to_DB(city_names_deque, cities_urls_deque, current_state)

            ## return cities_urls_deque
        
            print(f" {BLUE_COLOR }I'm starting to navigate to each city... {RESET_COLOR}")

                    
            ##============ for each city start grabbing agent details ==================
            # #cities = await get_city_urls_from_DB()
            # print(cities)
        

            ##================ update the DB once all the cities have been fetched ============================
            try:
                state_instance = await sync_to_async(all_states_links.objects.get)(
                    state_name__iexact=current_state.strip()
                )
            except all_states_links.DoesNotExist:
                print(f"State not found in the database.")
                return

            await sync_to_async(all_states_links.objects.filter(state_name=state_instance).update)(has_state_grabbed_all_urls=True)
            print(f'Updated {state_instance}')
            ## ========================================================================================================

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

         # we pause the script for a random interval
        random_delay = random.randint(3, 20)  
        print(f"lemme rest for {random_delay} seconds before exploring this city...")
        await asyncio.sleep(random_delay)

        await page.goto(current_url)

        code, c = current_url.replace('https://www.coldwellbanker.com/city/', '').split('/')[:2]
        state_code = code.upper()
        city = c.replace('-', ' ').title()
        city_name = city + ', ' + state_code

        print(f"I'm currently in {city_name}")     

        agent_names_list = []
        agent_phoneNumbers_list = []
        agent_emails_list = []
        agent_license_No_list = []
        agent_urls_list = []

        BASE_PERSONAL_URL = 'https://www.coldwellbanker.com'  

        ###============= checking presence of any agensts on the page=======
        MAX_RETRIES = 2  # Number of times to recheck
        RETRY_DELAY = 2  # Delay in seconds between retries

        for attempt in range(MAX_RETRIES + 1):  
            agent_locator_1 = page.get_by_test_id('emailLink')
            agent_locator_2 = page.get_by_test_id("office-name")

            if await agent_locator_2.count() > 0 or await agent_locator_1.count() > 0:
                print('Agents found')
                break  
            elif attempt < MAX_RETRIES:
                print(f'Retrying to locate agents... (attempted {attempt + 1}/{MAX_RETRIES})')
                await asyncio.sleep(RETRY_DELAY)
        else:
            print(f'{RED_COLOR} No agents founnd in {city_name} {RESET_COLOR}')
            try:
                city_instance = await sync_to_async(cities_real_estate_links.objects.get)(city_name=city_name.strip())
            except cities_real_estate_links.DoesNotExist:
                print(f"City '{city_name}' not found in the database.")
                return
            
            await sync_to_async(cities_real_estate_links.objects.filter(city_name=city_instance).update)(is_checked=True, agents_found_status='has no agents')

            print(f' {GREEN_COLOR}{city_instance}  updated {RESET_COLOR}')
            continue

        ### ==================================================
        while True:  # loop to handle pagination
            await asyncio.sleep(3) 

            ##======== extract agent details ===========================
            agent_name_locator = page.get_by_test_id("office-name")
            agent_names = await agent_name_locator.all_text_contents()

            phone_number_locator = page.get_by_test_id('phoneNumber')
            agent_phone_numbers = await phone_number_locator.all_text_contents()

            license_number_locator = page.get_by_test_id('license-number')
            agent_license_numbers = await license_number_locator.all_text_contents()

            email_locator = page.get_by_test_id('emailLink')
            if await email_locator.count() > 0:
                all_emails_locator = await email_locator.all()
            else:
                all_emails_locator = None
                continue
            # print(all_emails_locator)

            agent_URL_locator = page.get_by_test_id("basic-card") 
            agent_url_buttons = await agent_URL_locator.all()   # to click on agent for method 2
            agent_urls = await agent_URL_locator.evaluate_all(
                                              "(elements) => elements.map(el => el.getAttribute('href'))"
                                             )
            
            ##==== process agent details vigorously by clicking each profile ======================
            ## await process_agent_details_by_click(page, agent_url_buttons)
           
            ##=========================================================================================
            
            ## method 2
            # agent_url_locator = page.get_by_test_id("basic-card") 
            # agent_urls = [
            #         await locator.get_attribute('href') for locator in await agent_url_locator.element_handles()
            #     ]
            # for url in agent_urls:
            #     print(url)


            processed_emails = []
          
            if not agent_names:
                print(f"{GREEN_COLOR}No agents found on this page{RESET_COLOR}")
                # continue
            else:
                for mail in all_emails_locator:
                    try:
                        email = await mail.get_attribute('href')  
                        if email:
                            processed_email = email.replace('mailto:', "").strip()
                            processed_emails.append(processed_email)
                        else:
                            print(f"No email found for this agent")
                    except Exception as e:
                        print(f"{RED_COLOR}Error retrieving email: {e}{RESET_COLOR}")
                        continue  

                for agent_name, agent_phone_number, agent_email, agent_license_number, agent_link in zip_longest(agent_names, 
                                                                                               agent_phone_numbers,
                                                                                               processed_emails, 
                                                                                               agent_license_numbers,
                                                                                               agent_urls,
                                                                                               fillvalue=None):
                   
                    agent_url = BASE_PERSONAL_URL + agent_link
                    print(f"{agent_name} --> {agent_phone_number} - {agent_email} - {agent_license_number}-{agent_url}, {city_name}")
                    # print(city, state_code)
                                
                    agent_names_list.append(agent_name)
                    agent_phoneNumbers_list.append(agent_phone_number)
                    agent_emails_list.append(agent_email)
                    agent_license_No_list.append(agent_license_number)
                    agent_urls_list.append(agent_url)


                    ## ========== resting logic ============================================

                    pausing_break = 5
                    count_so_far = len(agent_names_list)
                    print(f'agents processed so far {count_so_far}')
                    if count_so_far % pausing_break == 0:
                         print(f"{MAGENTA_COLOR}Processed {count_so_far} agents. Taking a short break...{RESET_COLOR}")

                          # we pause the script for a random interval
                         random_delay = random.randint(2, 5)  
                         print(f"lemme rest for {random_delay} seconds before restarting...")
                         await asyncio.sleep(random_delay)

                    ##============================  end of resting =================================

            # ===== Logic for Next Page button ================================================
            try:
                next_page_button = page.get_by_test_id("NavigateNextIcon") 
                if await next_page_button.is_visible() and not await next_page_button.is_disabled():
                    

                    print(f"{BLUE_COLOR}Navigating to the next page...{RESET_COLOR}")
                    await next_page_button.hover()
                    await next_page_button.click()
                    # await page.wait_for_load_state('networkidle')  # Wait for the next page to load

                    # pausing_break = 5
                    # count_so_far = len(agent_names_list)
                    # print(f'agents processed so far {count_so_far}')
                    # if count_so_far % pausing_break == 0:
                    #      print(f"{MAGENTA_COLOR}Processed {count_so_far} agents. Taking a short break...{RESET_COLOR}")
                    #      await asyncio.sleep(10)

                else:
                    print(f"{RED_COLOR}No more pages to navigate,let me save first{RESET_COLOR}")


                    ## then update the agent profile details table
                    await save_agent_to_DB(agent_names_list, agent_phoneNumbers_list, agent_emails_list, 
                                                                                      agent_license_No_list,
                                                                                      agent_urls_list,
                                                                                      city_name
                                                                                      )
                    
                     # we pause the script for a random interval
                    random_delay = random.randint(5, 30)  
                    print(f"lemme rest for {random_delay} seconds before scraping vigorpously...")
                    await asyncio.sleep(random_delay)
                    
                    
                    ##========== to scrape each profile vigorously from urls acquired ===========================            
                    print('starting to scrape each profile vigorously')
                    await process_agent_details(page, agent_urls_list, state_code)
                    
                    # =================marrk the city as checked once done with a city====================================
                    try:
                        city_instance = await sync_to_async(cities_real_estate_links.objects.get)(
                            city_name=city_name.strip()
                        )
                    except cities_real_estate_links.DoesNotExist:
                        print(f"City '{city_name}' not found in the database.")
                        return

                    
                    total_agents_found = len(agent_urls_list)
                    await sync_to_async(cities_real_estate_links.objects.filter(city_name=city_instance).update)(is_checked=True, agents_found_status=total_agents_found)
                    print(f'{GREEN_COLOR} updated {city_instance} {RESET_COLOR}')
                    #### =================================================================================================
                    
                    ### update  no of cities done in a state
                    # all_states_links.objects
                    # print('updating city count in cuurent state')
                    # state_name = await sync_to_async(lambda: city_instance.state_name)()
                    # print(state_name)

                    # # Count the number of cities marked as checked for the state
                    # no_of_cities_done = await sync_to_async(cities_real_estate_links.objects.filter)(
                    #     state_name=state_name, is_checked=True
                    # )

                    ### mark that city as complete or already seen
                    print('-=========')
                    saved_data = [agent_names_list, agent_phoneNumbers_list, 
                                                    agent_emails_list, agent_license_No_list, agent_urls_list]
                    
                    ## log clearing each lists
                    for agent_list in saved_data:
                         agent_list.clear()      

   
                                                                                      
                    break
            except Exception as e:
                print(f"{RED_COLOR}Error with Next Page button: {e}{RESET_COLOR}")
                break
            # ===== End of Logic for Next Page button ================================================
            


async def save_agent_to_DB(agent_names_list, agent_phoneNumbers_list, agent_emails_list, agent_license_No_list, agent_urls_list, city_name):
    '''
    saves agent profile details to DB
    '''
  
    agents_object = [ Agent_profile_details(agent_name=agent_name, 
                                            agent_phone=agent_phone, 
                                            agent_email=agent_email,
                                            agent_license_number=agent_license_number,
                                            agent_url=agent_url,
                                            city_name=city_name
                                            )  
                    for agent_name, agent_phone, agent_email, agent_license_number, agent_url in zip_longest(agent_names_list, 
                                                                    agent_phoneNumbers_list, 
                                                                    agent_emails_list,
                                                                    agent_license_No_list,
                                                                    agent_urls_list,
                                                                    fillvalue=None
                                                                    )]


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
                state_name = state_names_deque.popleft() or "unknown state"
                state_url = state_urls_deque.popleft() or "unknown URL"
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
   
    # state_urls = await sync_to_async(list)(all_states_links.objects.filter(has_state_grabbed_all_urls=False).values_list('Link_to_real_estate', flat=True))
    # unprocessed_states = len(state_urls)

    # grab only unprocessed state URLs
    state_urls = await sync_to_async(list)(all_states_links.objects.filter(has_state_grabbed_all_urls=False).values_list("Link_to_real_estate", flat=True)
    )
    
    unprocessed_states = len(state_urls)
    print(f"{unprocessed_states} states to process.")

    # if not state_urls:
    #      state_urls = await sync_to_async(list)(all_states_links.objects.values_list('Link_to_real_estate', flat=True))


    #   return state_urls    ##  as a list
    return deque(state_urls)  # as a deque


async def save_cities_to_DB(city_names_deque, cities_urls_deque, current_state):
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

                try:
                     state_instance = await sync_to_async(all_states_links.objects.get)(state_name__iexact=current_state.strip())
                except all_states_links.DoesNotExist:
                        print(f"state deos not exist")
                        return
                
                await sync_to_async(cities_real_estate_links.objects.create)(city_name=city_name, link_to_city=city_url, state_name=state_instance)
                
                print(f" Saving {city_name} ->  {city_url}")

        print('Done processing')
            
    total_no_of_cities =  await sync_to_async(cities_real_estate_links.objects.count)()
    print(f" {total_no_of_cities} cities saved so far")
    #   return total_no_of_states


async def get_city_urls_from_DB():
    """
    returns the list of all city URLs from the DB
    """   
    
    city_urls = await sync_to_async(list)(cities_real_estate_links.objects.filter(is_checked=False).values_list("link_to_city", flat=True)
    )
    
    unprocessed_states = len(city_urls)
    print(f"{unprocessed_states} cities to process.")
   
    #   print(state_urls)

    #   return state_urls    ##  as a list
    return deque(city_urls)  # as a 



async def main():
    MAX_RETRIES = 3  
    RETRY_DELAY = 5 

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)   # remember if you set headless to true then enable(uncomment) the http headers below
        page = await browser.new_page()

        # ============ optional browser configurations==========================
        await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

        # await page.route("**/*.{jpg, png, jpeg}", lambda route: route.abort())   ### to hide photos
        # ================ end of browser configurations =============================
        BASE_URL = 'https://www.coldwellbanker.com/sitemap/agents'

        # await page.goto("http://127.0.0.1:8000/agents'")
        # await page.goto(BASE_URL)  
        # print(await page.title())

        ##============ Retry logic for navigating to the base URL===============#
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                await page.goto(BASE_URL, timeout=50000)  
                print(await page.title())
                break  
            except PlayWrightTimeoutError:
                print(f"Attempt {attempt} failed: Timeout while navigating to {BASE_URL}")
                if attempt < MAX_RETRIES:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    print(f"Failed to load {BASE_URL} after {MAX_RETRIES} attempts.")
                    await browser.close()
                    return

        # =====================================

        state_urls = await get_state_urls_from_DB()  ## retrieves URLs of  States from the DB

        if not state_urls:
            print("No state URLs found in the database. lemme grab from the webpage...")
            await grab_state_names(page, BASE_URL)  # Fetch state names and URLs
            state_urls = await get_state_urls_from_DB()  # now we can fethc the state urls from the DB

        print("Processing states to grab city data...")
        await grab_city_data_from_states(page, state_urls)

        city_urls = await get_city_urls_from_DB()    # getting URLs of each city to use grab profile details
        # print(city_urls)

        if not city_urls:
            print(f'{RED_COLOR}No cities found {RESET_COLOR}')          
        else:
             print(f" {GREEN_COLOR}{len(city_urls)} cities found {RESET_COLOR}")
             await grab_agent_profile_details(page, city_urls)
           
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())