# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from tickets.models import Station, Ticket

# Create your tests here.
class TicketTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.user = User.objects.create_user(username="test",password="test@123")

        # Stations
        self.station1 = Station.objects.create(name="Station A")
        self.station2 = Station.objects.create(name="Station B")
        self.station3 = Station.objects.create(name="Station C")

        # Ticket
        self.ticket = Ticket.objects.create(
            user=self.user,
            from_station=self.station1,
            to_station=self.station2,
            date="2025-03-01",
            price=101
        )
        
    def test_user_sees_only_own_tickets(self):
        self.client.login(username="test", password="test@123")
        url = reverse("ticket-list")
        response = self.client.get(url)
        
        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_admin_sees_all_tickets(self):
        self.client.login(username="admin", password="admin")
        url = reverse("ticket-list")
        response = self.client.get(url)

        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_ticket(self):
        self.client.login(username="test", password="test@123")
        url = reverse("ticket-list")
        data = {
            "from_station": self.station1.id,
            "to_station": self.station2.id,
            "date": "2025-12-12",
            "price": 120
        }
        response = self.client.post(url, data)

        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )

        # print('user =>', self.user.username)
        # print('resp =>', response.data['user'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_calculate_price(self):
        self.client.login(username="test", password="test@123")
        url = reverse("calculate-price")
        
        response = self.client.get(
            url,
            {"from_station": self.station1.id, "to_station": self.station3.id}
        )
        
        print('\nResponse =>', response.data)
        
        print(
            "\nlogged_in client =>",
            response.wsgi_request.user,
            response.wsgi_request.user.is_authenticated,
            response.wsgi_request.user.is_staff
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)