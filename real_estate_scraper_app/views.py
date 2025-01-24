from django.shortcuts import render
from rest_framework import permissions, viewsets

from real_estate_scraper_app.agent_profile_serializers import Agent_serializer, Agent_records_serializer
from .models import Agent_profile_details, Agent_records


# Create your views here.
class AgentViewSet(viewsets.ModelViewSet):
    """
    allows agents to be viewed
    """
    # queryset = Agent_profile_details.objects.all().order_by('agent_name')
    queryset = Agent_profile_details.objects.all()
    serializer_class = Agent_serializer
    # permission_classes = [permissions.IsAuthenticated]

class AgentRecordViewSet(viewsets.ModelViewSet):
    '''
    displays all the details of an agent
    '''
    queryset = Agent_records.objects.all()
    serializer_class = Agent_records_serializer

