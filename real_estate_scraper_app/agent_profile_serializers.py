from rest_framework import serializers
from .models import Agent_profile_details


class Agent_serializer(serializers.ModelSerializer):
    class Meta:
        model = Agent_profile_details
        fields = [
            'agent_name',
            'agent_phone'
            # 'id'
        ]



class State_serializer(serializers.HyperlinkedModelSerializer):
    pass