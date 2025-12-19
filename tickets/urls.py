from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, TicketViewSet, UserViewSet
from . import views

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"stations", StationViewSet)
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
    path("calculate-price/", views.calculate_price),
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
