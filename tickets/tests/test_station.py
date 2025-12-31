from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from tickets.models import Station
from tickets.serializers import StationSerializer

# initialize the APIClient app
client = Client()

class StationTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.user = User.objects.create_user(username="test", password="test@123")
        
        # Stations
        self.station1 = Station.objects.create(name="Mumbai")
        self.station2 = Station.objects.create(name="Pune")
        
        #urls
        self.list_url = reverse("station-list")
        self.detail_url = reverse("station-detail", args=[self.station1.id])
    
    # Authentication
    def test_authentication_valid(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)
    
    def test_authentication_invalid(self):
        login_success = client.login(username="test", password="test123")
        self.assertFalse(login_success)
        
        
    # GET
    # Public 
    def test_list_stations_public(self):
        response = client.get(self.list_url)
        
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_station_public(self):
        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.station1.name)


    # Private
    def test_list_stations(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)
        
        response = client.get(self.list_url)

        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_retrieve_station(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)
        
        response = client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.station1.name)
    
    # POST
    # Public
    def test_create_station_public(self):
        data = {"name": "Surat"}
        serializer = StationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        response = client.post(self.list_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    # Private
    def test_create_station(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)

        data = {"name": "Surat"}
        serializer = StationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        response = client.post(self.list_url, data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Station.objects.filter(name="Surat").exists())
    
    def test_create_station_duplicate_name(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)
        
        data = {"name": "Pune"}
        serializer = StationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        response = client.post(self.list_url, data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data) 
        
    def test_create_station_invalid(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)
        
        data={}
        serializer = StationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        response = client.post(self.list_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    # PUT
    # Public
    def test_update_station_public(self):
        data = {"name": "New Mumbai"}
        serializer = StationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        response = client.put(self.detail_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
    
    # Private
    def test_update_station(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)

        data = {"name": "New Mumbai"}
        serializer = StationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        response = client.put(self.detail_url, data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station1.refresh_from_db()
        self.assertEqual(self.station1.name, "New Mumbai")
    
    # DELETE
    # Public
    def test_delete_station(self):
        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Private
    def test_delete_station(self):
        login_success = client.login(username="test", password="test@123")
        self.assertTrue(login_success)

        response = client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Station.objects.filter(id=self.station1.id).exists())