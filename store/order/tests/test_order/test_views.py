from models import User
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from models import Order
from django.urls import reverse_lazy


class TestCaseModulOrder(TestCase):
    def setUp(self) -> None:
        user_data = {
            "password": "testAdmin",
            "username": "testAdmin",
            }
        self.user = User.objects.create_user(user_data)
        self.order = Order.objects.create(
            initiator=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            status='o',
            total_cost=0
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_active_orders(self):
        response = self.client.get(reverse_lazy('order:active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        data = {
            'initiator': self.user.id,
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.test",
            "address": "testAddress",
            "total_cost": 12.00
        }
        response = self.client.post(reverse_lazy('order:orders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_get_order_list_valid(self):
        response = self.client.get(reverse_lazy('order:orders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_detail_valid(self):
        response = self.client.get(reverse_lazy('order:orders-detail', args=(1, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_get_order_list_invalid_user(self):
        self.client.logout()
        with self.assertRaises(TypeError):
            self.client.get(reverse_lazy('order:orders-list'))

    def test_get_order_detail_invalid_code(self):
        response = self.client.get(reverse_lazy('order:orders-detail', args=(0, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
