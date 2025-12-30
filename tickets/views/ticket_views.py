# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from tickets.serializers import TicketSerializer
from tickets.models import Ticket, Station
from rest_framework.exceptions import ValidationError

# Protected views
class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="calculate-price")
    def calculate_price(self, request):
        params = request.query_params
        from_station = params.get("from_station")
        to_station = params.get("to_station")

        print("From id =>", from_station, type(from_station))

        if not from_station or not to_station:
            raise ValidationError(
                {"detail": "from_station and to_station are required"}
            )

        from_station_id = int(from_station)
        to_station_id = int(to_station)

        if from_station_id == to_station_id:
            raise ValidationError(
                {"detail": "from_station and to_station must be different"}
            )

        from_station_obj = Station.objects.get(id=from_station_id)
        to_station_obj = Station.objects.get(id=to_station_id)

        print("Station =>", from_station_obj, to_station_obj)

        price = abs(from_station_id - to_station_id) + 100

        return Response(
            {
                "from_station": from_station_obj.name,
                "to_station": to_station_obj.name,
                "price": price,
            }
        )


# Protected view
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def calculate_price(request):
    params = request.query_params
    from_station = params.get("from_station")
    to_station = params.get("to_station")

    print("From id =>", from_station, type(from_station))

    if not from_station or not to_station:
        raise ValidationError({"detail": "from_station and to_station are required"})

    from_station_id = int(from_station)
    to_station_id = int(to_station)

    if from_station_id == to_station_id:
        raise ValidationError(
            {"detail": "from_station and to_station must be different"}
        )

    from_station_obj = Station.objects.get(id=from_station_id)
    to_station_obj = Station.objects.get(id=to_station_id)

    print("Station =>", from_station_obj, to_station_obj)

    price = abs(from_station_id - to_station_id) + 100

    return Response(
        {
            "from_station": from_station_obj.name,
            "to_station": to_station_obj.name,
            "price": price,
        }
    )
