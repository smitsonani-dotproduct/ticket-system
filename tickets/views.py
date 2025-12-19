# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Station, Ticket
from .serializers import StationSerializer, TicketSerializer, UserSerializer


# Protected views & Read only viewset
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Public views + Only authenticated users can modify
class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrive"]:
            return []
        return [IsAuthenticated()]


# Protected views
class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ticket.objects.all()
        user = self.request.user
        if user.is_staff:
            return queryset
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="calculate-price")
    def calculate_price(self, request):
        qs = request.query_params
        from_station_id = qs.get("from_station")
        to_station_id = qs.get("to_station")

        if not from_station_id or not to_station_id:
            return Response(
                {"error": "from_station and to_station are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif from_station_id == to_station_id:
            return Response(
                {"error": "from_station and to_station must be different"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from_station_id = int(from_station_id)
            to_station_id = int(to_station_id)

            from_station = Station.objects.get(id=from_station_id)
            to_station = Station.objects.get(id=to_station_id)

            print("Station =>", from_station, to_station)

        except ValueError:
            return Response(
                {"error": "Station IDs must be integers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Station.DoesNotExist:
            return Response(
                {"error": "From station or To station not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        price = abs(from_station_id - to_station_id) + 100

        return Response(
            {
                "from_station": from_station.name,
                "to_station": to_station.name,
                "price": price,
            }
        )


# Protected view
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def calculate_price(request):
    qs = request.query_params
    from_station_id = qs.get("from_station")
    to_station_id = qs.get("to_station")

    if not from_station_id or not to_station_id:
        return Response(
            {"error": "from_station and to_station are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif from_station_id == to_station_id:
        return Response(
            {"error": "from_station and to_station must be different"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        from_station_id = int(from_station_id)
        to_station_id = int(to_station_id)

        from_station = Station.objects.get(id=from_station_id)
        to_station = Station.objects.get(id=to_station_id)

        print("Station =>", from_station, to_station)

    except ValueError:
        return Response(
            {"error": "Station IDs must be integers"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Station.DoesNotExist:
        return Response(
            {"error": "From station or To station not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    price = abs(from_station_id - to_station_id) + 100

    return Response(
        {
            "from_station": from_station.name,
            "to_station": to_station.name,
            "price": price,
        }
    )
