from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Package, Enquiry, ContactMessage, CustomQuote

class APITests(APITestCase):
    def setUp(self):
        self.package = Package.objects.create(
            title="Goa Holiday",
            itinerary="Day 1: Arrival, Day 2: Sightseeing",
            inclusions="Hotel, Breakfast",
            exclusions="Flights",
            price=15000.00,
            image="test_image.jpg"
        )

    def test_submit_enquiry(self):
        url = reverse('submit-enquiry')
        data = {
            'package': self.package.id,
            'name': 'John Doe',
            'phone': '1234567890',
            'email': 'john@example.com',
            'travel_dates': '2026-09-01',
            'number_of_people': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submit_contact(self):
        url = reverse('submit-contact')
        data = {
            'name': 'Jane Doe',
            'phone': '0987654321',
            'email': 'jane@example.com',
            'message': 'Hello world'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_submit_quote(self):
        url = reverse('submit-quote')
        data = {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'phone': '5555555555',
            'service_type': 'Tour Package',
            'destination': 'Kerala',
            'travel_date': '2026-10-10',
            'duration': '5',
            'adults': '2',
            'children': '1',
            'budget': '30000',
            'message': 'Need customized itinerary'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

