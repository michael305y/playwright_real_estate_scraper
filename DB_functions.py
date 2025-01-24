from itertools import zip_longest
from time import sleep
import django
import os
import asyncio
from collections import deque
from playwright.async_api import async_playwright
from asgiref.sync import sync_to_async

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_scraper_project.settings")
django.setup()

from real_estate_scraper_app.models import Agent_records

from real_estate_scraper_app.styling_colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, RESET_COLOR, MAGENTA_COLOR

async def save_detailed_agent_records_to_DB(names_list, license_list, phone_list, email_list, 
                                                                                spoken_language_list, 
                                                                                agent_office_location_list,
                                                                                agent_about_info_list,
                                                                                IG_link_list,
                                                                                FB_link_list,
                                                                                twitter_link_list,
                                                                                agent_designations_list,
                                                                                agent_website_list,
                                                                                agent_role_list,
                                                                                google_map_link_list,
                                                                                current_listings_list,
                                                                                state_code
                                                                                ):

     '''
     saves detailed agent records to DB
     '''
     agent_object = [Agent_records(agent_name=agent_name,
                                   agent_license=agent_license,
                                   agent_phone=agent_phone,
                                   agent_email=agent_email,
                                   spoken_language=spoken_language,
                                   agent_office_location=agent_office_location,
                                   agent_about_info=agent_about_info,
                                   IG_link=IG_link,
                                   FB_link=FB_link,
                                   Twitter_link=Twitter_link,
                                   agent_designations=agent_designations,
                                   agent_website=agent_website,
                                   agent_role=agent_role,
                                   google_map_link=google_map_link,
                                   current_listings=current_listings,
                                   state_code=state_code
                                   ) 
                                   
                                   for agent_name, agent_license, agent_phone, 
                                                        agent_email, 
                                                        spoken_language, 
                                                        agent_office_location, 
                                                        agent_about_info, 
                                                        IG_link,
                                                        FB_link,
                                                        Twitter_link,
                                                        agent_designations,
                                                        agent_website,
                                                        agent_role,
                                                        google_map_link,
                                                        current_listings
                                                           
                                                                    in zip_longest(names_list, 
                                                                          license_list,
                                                                          phone_list,
                                                                          email_list,
                                                                          spoken_language_list,
                                                                          agent_office_location_list,
                                                                          agent_about_info_list,
                                                                          IG_link_list,
                                                                          FB_link_list,
                                                                          twitter_link_list,
                                                                          agent_designations_list,
                                                                          agent_website_list,
                                                                          agent_role_list,
                                                                          google_map_link_list,
                                                                          current_listings_list,
                                                                          fillvalue=None
                                                                          )]
                                  

     await sync_to_async(Agent_records.objects.bulk_create)(agent_object)

     await asyncio.sleep(2)

     total_agent_count = await sync_to_async(Agent_records.objects.count)()
     print(f' {BLUE_COLOR} {total_agent_count} agents saved {RESET_COLOR}')
