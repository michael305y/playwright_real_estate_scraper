from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Agent_profile_details(models.Model):
    agent_name = models.CharField(max_length=200,  null=True, blank=True, default="No agent name Found")
    agent_phone = models.CharField(max_length=200,  null=True, blank=True, default="No Phone Found")  # make it a string
    agent_email = models.EmailField( null=True, blank=True, default="No Email Found")
    agent_license_number = models.CharField(max_length=200, null=True, blank=True, default="No License Found")
    agent_url= models.URLField()
    city_name = models.CharField(max_length=200,  null=True, blank=True, default=" ")
    # date_created = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.agent_name}"
    
    
class Agent_records(models.Model):
    agent_name = models.CharField(max_length=200, null=True, blank=True, default="No name Found")
    agent_license = models.CharField(max_length=300, null=True, blank=True, default="No License Found")
    agent_phone = models.CharField(max_length=300, null=True, blank=True, default="No Phone Found")
    agent_email = models.EmailField(null=True, blank=True, default="No Email Found")
    spoken_language = models.CharField(max_length=500, null=True, blank=True, default="No Language Found")
    agent_office_location = models.CharField(max_length=500, null=True, blank=True, default="No Office Found")
    agent_about_info = models.TextField(null=True, blank=True, default="No About Info Found")
    IG_link = models.URLField(null=True, blank=True, default="No IG Found")
    FB_link = models.URLField(null=True, blank=True, default="No FB Found")
    Twitter_link = models.URLField(null=True, blank=True, default="No X Found")
    agent_designations = models.TextField(null=True, blank=True, default="No Designation Info Found")
    agent_website = models.URLField(null=True, blank=True, default='No agent website')
    agent_role = models.CharField(max_length=500, null=True, blank=True, default="No Role Found")
    google_map_link = models.CharField(max_length=500, null=True, blank=True, default="No map link Found")
    current_listings = models.TextField(null=True, blank=True, default="No Homes or Listings Found")
    state_code = models.CharField(max_length=100, null=True, blank=True, default=" ")



    def __str__(self):
        return f"{self.agent_name}"


class all_states_links(models.Model):
    state_name = models.CharField(max_length=200)
    Link_to_real_estate = models.URLField()
    has_state_grabbed_all_urls = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.state_name}"

class cities_real_estate_links(models.Model):
    city_name = models.CharField(max_length=200)
    link_to_city = models.URLField()
    state_name = models.ForeignKey(all_states_links, on_delete=models.CASCADE, null=True, blank=True, related_name="cities")
    is_checked = models.BooleanField(default=False)  ## checks whether a city has been processed whether agents are or not found
    agents_found_status = models.CharField(max_length=200, null=True, blank=True, default="No Agents Found")
    urls_with_errors = models.TextField(null=True, blank=True, default=" ")

    def __str__(self):
        return f"{self.city_name}"


class AgentURLWithError(models.Model):
    agent_name = models.CharField(max_length=200, null=True, blank=True, default="No name Found" )
    urls_with_errors = models.TextField(null=True, blank=True, default=" ", help_text="agent url failed to process")

    def __str__(self):
        return f"{self.agent_name}"

