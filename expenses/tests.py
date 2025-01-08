

from rest_framework.test import APITestCase
from rest_framework import status
from .models import Expense, Group, User

class ExpenseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = Group.objects.create(name="Test Group")
        self.group.members.add(self.user)

    def test_create_expense(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "amount": 100,
            "category": 1,  
            "split_type": "equal",
            "date": "2025-01-01",
            "group": self.group.id,
        }
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
