from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, TicketViewSet, UserViewSet, calculate_price
# from . import views

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"stations", StationViewSet, basename="station")
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
    path("calculate-price/", calculate_price, name='calculate-price'),
]

# # Station APIs

# GET /api/stations/
# POST /api/stations/
# PUT /api/stations/{id}/
# DELETE /api/stations/{id}/

# # Ticket APIs

# GET /api/tickets/
# POST /api/tickets/
# GET /api/tickets/{id}/
