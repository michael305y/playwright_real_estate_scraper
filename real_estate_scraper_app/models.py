from django.db import models

# Create your models here.
class Agent_profile_details(models.Model):
    agent_name = models.CharField(max_length=200)
    agent_phone = models.CharField(max_length=200)  # make it a string
    agent_email = models.EmailField()
    agent_license_number = models.CharField(max_length=200, null=True, blank=True, default="No License Found")
    # date_created = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.agent_name}"
    

class all_states_links(models.Model):
    state_name = models.CharField(max_length=200)
    Link_to_real_estate = models.URLField()

    def __str__(self):
        return f"{self.state_name}"

class cities_real_estate_links(models.Model):
    city_name = models.CharField(max_length=200)
    link_to_city = models.URLField()

    def __str__(self):
        return f"{self.city_name}"

