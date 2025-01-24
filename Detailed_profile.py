"""
Grabs the profile details of each agent:
1. Name
2. Phone number
3. Email
4. Social media links
5. Spoken languages
6. State code or state name
7. City name
8. Address
9. About Info
"""


from collections import deque
import time 
from playwright.sync_api import sync_playwright

import asyncio
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError as PlayWrightTimeoutError
from asgiref.sync import sync_to_async

from real_estate_scraper_app.styling_colors import GREEN_COLOR, RESET_COLOR

from DB_functions import save_detailed_agent_records_to_DB
from real_estate_scraper_app.models import Agent_profile_details, AgentURLWithError, cities_real_estate_links


async def grab_agent_profile_details_2(page):
    '''
    grabs agent details in depth from the specified web page by locating the specified elements
    '''
    
    try:
        ## 1) method 1 agent name from title  more stable
        page_title = await page.title()
        if page_title == '502 Bad Gateway':
            agent_name_locator = page.locator('h1.MuiTypography-root.MuiTypography-h4.css-9dw3oo-MuiTypography-root')
            agent_name = await agent_name_locator.text_content()
        else:
            agent_name = page_title.replace('- Real Estate Agent - Coldwell Banker', ' ').strip()
        print(agent_name)
    except PlayWrightTimeoutError as e:
        print(f'error locating element {e}')


    license_locator = page.get_by_test_id("basicMedia").get_by_test_id("licenses")
    if await license_locator.count() > 0:
        agent_license_No = await license_locator.text_content()  
    else:
        agent_license_No = None
    print(agent_license_No)
   
    agent_phone_number_locator = page.get_by_test_id('office-phone-tablet')
    agent_phone = await agent_phone_number_locator.text_content()
    print(agent_phone)

    agent_email_tablet_locator = page.get_by_test_id('agent-mail-tablet')
    email = await agent_email_tablet_locator.text_content()
    print(email)

    agent_spoken_languanges_locator = page.locator('p.MuiTypography-root.MuiTypography-body1.Languages_spoken__tXtAZ')
    if await agent_spoken_languanges_locator.count() > 0:
        spoken_language = await agent_spoken_languanges_locator.text_content()
    else:
        spoken_language = 'No Spoken language Found'
    print(spoken_language)

    try:
         agent_office_and_location_locator = page.locator('div.MuiStack-root.css-l5c1s3')
         if await agent_office_and_location_locator.count() > 0:
           location = await agent_office_and_location_locator.all_inner_texts()
           agent_office_location = location[0].split('\n\n')[1]
           print(agent_office_location) 
         else:
             agent_office_location = 'No agent office found'
         print(agent_office_location)
    except Exception as e:
        print({e})

    agent_about_info_locator = page.locator('#demo-customized-menu')   # either use this 1) more accurate but flaky
    # agent_about_info_locator = page.get_by_test_id('AgentProfile')       # 2) lessaccurate
    if await agent_about_info_locator.count() > 0:
        info = await agent_about_info_locator.text_content()
    else:
        info = 'No About info Found'
    print(info)

    ## ====================social media links ========================================
    agent_IG_link_locator  =  page.get_by_test_id("basicMedia").get_by_role("link", name="instagram")  # sometines works on headed mode
    if await agent_IG_link_locator.count() > 0:
        IG_link = await agent_IG_link_locator.get_attribute('href')
    else:
        IG_link = 'No IG info Found'
    print(IG_link)

    agent_FB_link_locator  =  page.get_by_test_id("basicMedia").get_by_role("link", name="facebook")  # sometimes works on headed mode
    if await agent_FB_link_locator.count() > 0:
        FB_link = await agent_FB_link_locator.get_attribute('href')
    else:
        FB_link = 'No about FB info Found'
    print(FB_link)

    agent_twitter_link_locator  =  page.get_by_test_id("basicMedia").get_by_role("link", name="twitter")  # only works on headed mode
    if await agent_twitter_link_locator.count() > 0:
        twitter_link = await agent_twitter_link_locator.get_attribute('href')
    else:
        twitter_link = 'No about Twitter info Found'
    print(twitter_link)
#     # =================================end of social media linsk ==========================

    agent_designation_locator = page.locator('li.Designations_underorderListItem__M092N')
    agent_designations =  await agent_designation_locator.all_text_contents()
    print(agent_designations)

    agent_website_locator = page.get_by_test_id("business-websiteurl-tablet")
    if await agent_website_locator.count() > 0:
        agent_website = await agent_website_locator.get_attribute('href')
    else:
        agent_website = 'No webiste'
    print(agent_website)

    agent_role_locator = page.locator("li:is(.MuiTypography-root.MuiTypography-body1, .MuiTypography-root.MuiTypography-body2)")
    if await agent_role_locator.count() > 0:
        agent_role = await agent_role_locator.first.text_content()
    else:
        agent_role = "Role not found"
    print(agent_role)

    agent_google_map_link_office_locator = page.get_by_test_id('google-map-link2')
    google_map_link =  await agent_google_map_link_office_locator.all_text_contents()
    print(google_map_link)

    Homes_for_sale_locator = await page.get_by_test_id("card-content").get_by_test_id('price').count()

    if  Homes_for_sale_locator > 0:
        agent_current_listing_prices_locator = page.get_by_test_id("card-content").get_by_test_id('price')
        agent_listing_property_details_locator = page.get_by_test_id("card-content").locator('div.MuiTypography-root.MuiTypography-body1')
        agent_listing_property_location_locator = page.get_by_test_id("card-content").locator('div.MuiTypography-root.MuiTypography-body3')
        
        agent_current_listing_prices = await agent_current_listing_prices_locator.all_text_contents()
        agent_listing_property_details = await agent_listing_property_details_locator.all_text_contents()
        agent_listing_property_location = await agent_listing_property_location_locator.all_text_contents()
        agent_listing_property_location = [item for item in agent_listing_property_location if not item.startswith('MLS#')]

        Home_for_sale = Homes_for_sale_locator
        str(Home_for_sale)
        listings = await process_listings(agent_current_listing_prices, agent_listing_property_details, agent_listing_property_location)
        
        # Append the number of homes for sale to the final return value
        current_listings = f"{Home_for_sale} Homes for sale\n"
        current_listings += f"{listings}\n"
    else:
        current_listings = 'No listing Found'
    print(current_listings)

    return agent_name, agent_license_No, agent_phone, email, spoken_language, agent_office_location, info, IG_link, FB_link, twitter_link, agent_designations, agent_website, agent_role, google_map_link, current_listings
    

async def process_listings(*args):
    """
    combines the all currentlistings found associated with an agent
    """
    all_current_listings = []
    agent_listing_property_location, agent_listing_properties, agent_current_listing_prices = args

    for listing_location, price, listing_properties in zip(agent_current_listing_prices, 
                                                           agent_listing_property_location, 
                                                           agent_listing_properties):
        
        current_homes_for_sale = f"-> A {price} home in {listing_location} with ({listing_properties})."
        # print(current_homes_for_sale)
        all_current_listings.append(current_homes_for_sale)

    # print(all_current_listings)
    return all_current_listings
    # print('processed all current listings')


async def process_agent_details(page, get_agent_urls, state_code):
    '''
    processes agent details vigorouly
    uses grab_agent_profile_details_2() to locate elemensts
    '''
    print(f'agent============ {state_code}')
    # urls = await get_agent_urls_from_DB()
    urls = deque(get_agent_urls)
    total_urls = len(urls)
    print(f' found {total_urls} profile urls')

    names_list = []
    license_list = []
    phone_list = []
    email_list = []
    spoken_language_list = []
    agent_office_location_list = [] 
    about_info_list = []
    IG_link_list = []
    FB_link_list = []
    twitter_link_list = []
    agent_designations_list = []
    agent_website_list = []
    agent_role_list = []
    google_map_link_list = []
    current_listings_list = []


    urls_checked_list = []
    urls_with_errors_list = []

    ## 1) ============== all at once =====================
    # while urls:
    #     current_url = urls.popleft()
    #     try:
    #         await page.goto(current_url)
    #         print(f"Processing URL: {current_url}")
    #         # Replace with your processing logic
    #         await grab_agent_profile_details_2(page)
    #         # await process_url(current_url)
    #     except Exception as e:
    #         print(f"Error processing {current_url}: {e}")
    #         ## no of urls not processed to be captured and saved/marked as not processed

    #         continue
    #     await asyncio.sleep(2)

    #     print('next person ====')
    ##============ processing all at one ======================

    ## 2) ======= to use batch to process ========================= 
    page_size = 12  # number of agents per page
    print(f"Total URLs: {total_urls}")

    no_of_batches = total_urls / page_size
    print(f' {no_of_batches} pages to process')
    done_batches = 0
    done_batches_list = []
    while urls:
        # process a batch of URLs(12 each)
        batch = [urls.popleft() for _ in range(min(page_size, len(urls)))]
        print(f"Processing batch: {len(batch)}")

        for current_url in batch:
            try:
                await page.goto(current_url)
                print(f"Processing URL: {current_url}")
                
                (
                    agent_name,
                    agent_license_No,
                    agent_phone,
                    agent_email,
                    spoken_language,
                    agent_office_location,
                    info,
                    IG_link,
                    FB_link,
                    twitter_link,
                    agent_designations,
                    agent_website,
                    agent_role,
                    google_map_link,
                    current_listings

                                   )  = await grab_agent_profile_details_2(page)
                
                if not agent_name:
                      print(f"{GREEN_COLOR}No agent found {RESET_COLOR}")
                      continue
                else:
                    # print(agent_license_No)
                    names_list.append(agent_name)
                    license_list.append(agent_license_No)
                    phone_list.append(agent_phone)
                    email_list.append(agent_email)
                    spoken_language_list.append(spoken_language)
                    agent_office_location_list.append(agent_office_location)
                    about_info_list.append(info)
                    IG_link_list.append(IG_link)
                    FB_link_list.append(FB_link)
                    twitter_link_list.append(twitter_link)
                    agent_designations_list.append(agent_designations)
                    agent_website_list.append(agent_website)
                    agent_role_list.append(agent_role)
                    google_map_link_list.append(google_map_link)
                    current_listings_list.append(current_listings)


                 ## update the urls have been completed
                urls_checked_list.append(current_url)   #### i'll check this later and work on it
               
            except Exception as e:
                print(f"Error processing {current_url}: {e}")

                name = current_url.split('/agents/')[1].split('/aid-')[0].replace('-', ' ').title()
                print(name)

                urls_with_error = current_url
                urls_with_errors_list.append(f' {urls_with_error} -> {e}')

                await sync_to_async(AgentURLWithError.objects.create)(agent_name=name, urls_with_errors=urls_with_error)
             
                continue        

        done_batches += len(batch)
        done_batches_list.append(batch)
       
        print(f'so far done {len(done_batches_list)} batch')
        if done_batches > 1:
            await asyncio.sleep(2)
            print("saving to DB")
            # print(names_list)

            await save_detailed_agent_records_to_DB(names_list, 
                                                    license_list,
                                                    phone_list, 
                                                    email_list, 
                                                    spoken_language_list,
                                                    agent_office_location_list,
                                                    about_info_list,
                                                    IG_link_list,
                                                    FB_link_list,
                                                    twitter_link_list,
                                                    agent_designations_list,
                                                    agent_website_list,
                                                    agent_role_list,
                                                    google_map_link_list,
                                                    current_listings_list,
                                                    state_code
                                                    )   
                                            

            # saved_data = [names_list,]
            # for data_list in saved_data:
            #     data_list.clear()

            done_batches_list.clear()
            names_list.clear()
            license_list.clear()
            phone_list.clear()
            email_list.clear()
            spoken_language_list.clear()
            agent_office_location_list.clear()
            about_info_list.clear()
            IG_link_list.clear()
            FB_link_list.clear()
            twitter_link_list.clear()
            agent_designations_list.clear()
            agent_website_list.clear()
            agent_role_list.clear()
            google_map_link_list.clear()
            current_listings_list.clear()

            

    ## ============== end of batch processing=========================


async def process_agent_details_by_click(page, agent_url_buttons):
    '''
    process urls by clicking
    '''
    

    names_list = []
    license_list = []
    phone_list = []
    email_list = []
    spoken_language_list = []
    agent_office_location_list = [] 
    about_info_list = []
    IG_link_list = []
    FB_link_list = []
    twitter_link_list = []
    agent_designations_list = []
    agent_website_list = []
    agent_role_list = []
    google_map_link_list = []
    current_listings_list = []

    
    for agent_profile in agent_url_buttons:
            await agent_profile.click()
            await asyncio.sleep(3)
            try:
                await asyncio.sleep(3)
                
                (
                    agent_name,
                    agent_license_No,
                    agent_phone,
                    agent_email,
                    spoken_language,
                    agent_office_location,
                    info,
                    IG_link,
                    FB_link,
                    twitter_link,
                    agent_designations,
                    agent_website,
                    agent_role,
                    google_map_link,
                    current_listings

                                   )  = await grab_agent_profile_details_2(page)

                names_list.append(agent_name)
                license_list.append(agent_license_No)
                phone_list.append(agent_phone)
                email_list.append(agent_email)
                spoken_language_list.append(spoken_language)
                agent_office_location_list.append(agent_office_location)
                about_info_list.append(info)
                IG_link_list.append(IG_link)
                FB_link_list.append(FB_link)
                twitter_link_list.append(twitter_link)
                agent_designations_list.append(agent_designations)
                agent_website_list.append(agent_website)
                agent_role_list.append(agent_role)
                google_map_link_list.append(google_map_link)
                current_listings_list.append(current_listings)
               
            except Exception as e:
                print(f"Error processing {agent_profile}: {e}")
                continue
        

            await save_detailed_agent_records_to_DB(names_list, 
                                                    license_list,
                                                    phone_list, 
                                                    email_list, 
                                                    spoken_language_list,
                                                    agent_office_location_list,
                                                    about_info_list,
                                                    IG_link_list,
                                                    FB_link_list,
                                                    twitter_link_list,
                                                    agent_designations_list,
                                                    agent_website_list,
                                                    agent_role_list,
                                                    google_map_link_list,
                                                    current_listings_list
                                                    )   
                                            
           

            
            names_list.clear()
            license_list.clear()
            phone_list.clear()
            email_list.clear()
            spoken_language_list.clear()
            agent_office_location_list.clear()
            about_info_list.clear()
            IG_link_list.clear()
            FB_link_list.clear()
            twitter_link_list.clear()
            agent_designations_list.clear()
            agent_website_list.clear()
            agent_role_list.clear()
            google_map_link_list.clear()
            current_listings_list.clear()
            await page.go_back()
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(2)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()  

        ### for testing the functioning of this module
        PERSONAL_URLS = [
            'https://www.coldwellbanker.com/il/schaumburg/agents/aleya-abdulawal/aid-P00200000GXKzUvdvzi5AxiL2H0KZGRJ4EVDzmid',
            # 'https://www.coldwellbanker.com/ma/city-unavailable/agents/dan-aaron/aid-P00200000GPBwKsOUgLGNiSKcpj6Fbhfj6GtuxG7',
            'https://www.coldwellbanker.com/il/long-grove/agents/sandee-abern/aid-P00200000FSk1BEWme338RGzrg5kCVa6v0baoU9X',
            'https://www.coldwellbanker.com/ma/haverhill/agents/marybeth-abate/aid-P00200000FSk0ZHNmCbWFfTtVy5r29HRwdvPXohK',
            'https://www.coldwellbanker.com/al/dothan/agents/bobby-estes/aid-P00200000FDdsKnjVBLDHhyDgFtEyG6vLLjqTnic',
            'https://www.coldwellbanker.com/il/edwardsville/agents/abid-ali/aid-P00200000FDdqn3n7SLvMeszlA1RXtQWRUaS3IS9',
            'https://www.coldwellbanker.com/ct/orange/agents/farhat-abbas/aid-P00200000GOyXxlI5GT4tweLNjG3GkX9toEAmAeG',
            'https://www.coldwellbanker.com/ca/huntington-beach/agents/fay-abed/aid-P00200000FegXntYZ4oo4SjEyD9TK2CrXlavw23s'
          ]

        # if headless mode:  # uncomment the below hhtp headers
        await page.set_extra_http_headers({
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

        ## uncommnent o the following only when testing
        # await page.goto(PERSONAL_URL)
        # print(await page.title())

        ## await process_agent_details(page, get_agent_urls_from_DB)

        # await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

