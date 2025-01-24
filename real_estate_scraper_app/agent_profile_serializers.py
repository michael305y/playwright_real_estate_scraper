from rest_framework import serializers
from .models import Agent_profile_details, Agent_records


class Agent_serializer(serializers.ModelSerializer):
    class Meta:
        model = Agent_profile_details
        fields = [
            'agent_name',
            'agent_phone'
            # 'id'
        ]


class Agent_records_serializer(serializers.ModelSerializer):
    class Meta:
        model = Agent_records
        fields = [
               'agent_name',
               'agent_license',       
               'agent_phone',
               'agent_email',
               'spoken_language',
               'agent_office_location',
               'agent_about_info',
               'IG_link',
               'FB_link',
               'Twitter_link',
               'agent_designations',
               'agent_website',
               'agent_role',
               'current_listings'


        ]


class State_serializer(serializers.HyperlinkedModelSerializer):
    pass