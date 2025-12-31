from rest_framework import serializers
from tickets.models import Station

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name"]
