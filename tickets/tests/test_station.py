# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from tickets.serializers import UserSerializer, StationSerializer, TicketSerializer
from tickets.models import Station, Ticket

# Create your tests here.
class StationTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.user = User.objects.create_user(username="test", password="test@123")

        # Stations
        self.station1 = Station.objects.create(name="Station A")
        self.station2 = Station.objects.create(name="Station B")

    
    def test_list_stations(self):
        url = reverse("station-list")
        response = self.client.get(url)

        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_station(self):
        login_success = self.client.login(username="test", password="test@123")
        self.assertTrue(login_success)
        url = reverse("station-list")
        response = self.client.post(url, {"name": "Station X"})

        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        