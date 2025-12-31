from rest_framework import serializers
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Ticket
        fields = ["id", "user", "from_station", "to_station", "date", "price"]

    def validate(self, data):
        from_station = data.get("from_station")
        to_station = data.get("to_station")

        if from_station == to_station:
            raise serializers.ValidationError(
                {"non_field_errors": ["From station and To station must be different"]}
            )

        return data