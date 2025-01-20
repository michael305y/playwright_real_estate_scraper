from django.contrib import admin
from .models import Agent_profile_details, all_states_links, cities_real_estate_links

# Register your models here.
admin.site.register(Agent_profile_details)
admin.site.register(all_states_links)
admin.site.register(cities_real_estate_links)


