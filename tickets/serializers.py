from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Station, Ticket


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name"]


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Ticket
        fields = ["id", "user", "from_station", "to_station", "date", "price"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
        ]
