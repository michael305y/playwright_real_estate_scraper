from django.contrib import admin
from .models import Agent_profile_details, all_states_links, cities_real_estate_links, Agent_records, AgentURLWithError
from import_export.admin import ExportMixin, ImportExportModelAdmin
from .agent_export_resources import AgentsRecordExportResource

# Register your models here.

## ============= NATIVE ADMIN SETTINGS ====================================
# admin.site.register(Agent_profile_details)
admin.site.register(all_states_links)
# admin.site.register(cities_real_estate_links)  ### we make it modifiable
# admin.site.register(Agent_records)
admin.site.register(AgentURLWithError)
#=========================================================================


##============== customization of admin ===========================
## export functionality
@admin.register(Agent_profile_details)
class AgentProfilelAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('agent_name', 'agent_email', 'agent_phone')  # Fields to display in the list view
    search_fields = ('agent_name', 'agent_email')   # our search fields


@admin.register(Agent_records)
class DetailedAgentRecordsAdmin(ImportExportModelAdmin):
    resource_class = AgentsRecordExportResource


##=============== to make our state field readonly
@admin.register(cities_real_estate_links)
class CitiesRealEstateLinksAdmin(admin.ModelAdmin):
    readonly_fields = ('state_name',)

    def get_readonly_fields(self, request, obj=None):
        # Make 'state' read-only only for existing objects
        if obj:  # Editing an existing city
            return ('state_name',)
        return super().get_readonly_fields(request, obj)

