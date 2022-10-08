from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.
class UserTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('example', 'example@email.com', 'somepassword')
        self.create_url = reverse('account-create')
    
    def test_create_user(self):

        data = {
            'username': 'foobar',
            'email': 'foobar@email.com',
            'password': 'nicepassword'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertFalse('password' in response.data)

    def test_short_password(self):
        
        data = {
            'username': 'foobar',
            'email': 'foobar@email.com',
            'password': 'nice'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)
    
    def test_no_password(self):
        
        data = {
            'username': 'foobar',
            'email': 'foobar@email.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)