from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

from ..models import User


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_list = reverse('all-user')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),            
            'password': "admin@123",
            'first_name': self.fake.email().split('@')[0],
            'last_name': self.fake.email().split('@')[1],
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()