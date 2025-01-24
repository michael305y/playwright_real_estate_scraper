from import_export import resources
from .models import Agent_records

class AgentsRecordExportResource(resources.ModelResource):
    class Meta:
        model = Agent_records
        fields = ('agent_name', 'agent_phone','state_code','agent_license', 'spoken_language', 'agent_role', 'current_listings')