from datetime import date

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from tickets.models import Station, Ticket
from tickets.serializers import TicketSerializer

# initialize the APIClient app
client = Client()

# Create your tests here.
class TicketTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.user1 = User.objects.create_user(username="test1",password="test@123")
        self.user2 = User.objects.create_user(username="test2",password="test@123")

        # Stations
        self.station1 = Station.objects.create(name="Mumbai")
        self.station2 = Station.objects.create(name="Delhi")
        self.station3 = Station.objects.create(name="Pune")

        # Tickets
        self.ticket1 = Ticket.objects.create(
            user=self.user1,
            from_station=self.station1,
            to_station=self.station2,
            date=date.today(),
            price= 100 + abs(self.station2.id - self.station1.id),
        )
        self.ticket2 = Ticket.objects.create(
            user=self.user2,
            from_station=self.station2,
            to_station=self.station3,
            date=date.today(),
            price=100 + abs(self.station3.id - self.station2.id),
        )
        self.ticket3 = Ticket.objects.create(
            user=self.user1,
            from_station=self.station1,
            to_station=self.station3,
            date=date.today(),
            price= 100 + abs(self.station2.id - self.station1.id),
        )
        
        # urls
        self.list_url = reverse("ticket-list")
        self.detail_url = reverse("ticket-detail", args=[self.ticket1.id])
        self.calculate_price_url = reverse("ticket-calculate-price")

    # Public
    def test_ticket_list_public(self):
        response = client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_calculate_price_public(self):
        params = {"from_station": self.station1.id, "to_station": self.station3.id}
        response = client.get(self.calculate_price_url, params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_ticket_public(self):
        data = {
            "from_station": self.station1.id,
            "to_station": self.station2.id,
            "date": "2025-12-12",
            "price": 100 + abs(self.station1.id-self.station2.id)
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Private
    def test_user_sees_only_own_tickets(self):
        login_success = client.login(username="test1", password="test@123")
        self.assertTrue(login_success)

        response = client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.ticket1.id)
        
    def test_admin_sees_all_tickets(self):
        login_success = client.login(username="admin", password="admin")
        self.assertTrue(login_success)

        response = client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
    def test_create_ticket_same_station_invalid(self):
        login_success = client.login(username="admin", password="admin")
        self.assertTrue(login_success)
        
        data = {
            "from_station": self.station1.id,
            "to_station": self.station1.id,
            "date": date.today(),
            "price": 100,
        }
        response = client.post(self.list_url, data, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
    
    def test_calculate_price_same_station_invalid(self):
        login_success = client.login(username="test1", password="test@123")
        self.assertTrue(login_success)

        params = {"from_station": self.station1.id, "to_station": self.station1.id}
        response = client.get(self.calculate_price_url, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_calculate_price(self):
        login_success = client.login(username="test1", password="test@123")
        self.assertTrue(login_success)
        
        params = {"from_station": self.station1.id, "to_station": self.station3.id}
        response = client.get(self.calculate_price_url, params)
        
        price = abs(self.station3.id - self.station1.id) + 100
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("price", response.data)
        self.assertEqual(response.data["price"], price)
        
    def test_calculate_price_missing_params_invalid(self):
        login_success = client.login(username="test2", password="test@123")
        self.assertTrue(login_success)

        response = client.get(self.calculate_price_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_ticket(self):
        login_success = client.login(username="test2", password="test@123")
        self.assertTrue(login_success)

        data = {
            "from_station": self.station1.id,
            "to_station": self.station2.id,
            "date": "2025-12-12",
            "price": 100 + abs(self.station1.id-self.station2.id)
        }
        response = client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)