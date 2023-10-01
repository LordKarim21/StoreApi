from order.models import Order
from user.models import User
from product.models import Basket

from django.test import TestCase


class TestCaseModulOrder(TestCase):
    def setUp(self) -> None:
        user_data = {
            "password": "testAdmin",
            "username": "testAdmin",
            }
        self.user = User.objects.create_user(user_data)
        self.order = Order.objects.create(initiator=self.user, full_name="test test",
                                          email="test@test.test", address="testAddress", total_cost=12.00)

    def test_exists_user_and_order(self):
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.order.id, 1)

    def test_update_after_payment(self):
        self.assertEqual(self.order.status, 'o')
        self.order.update_after_payment()
        self.assertEqual(self.order.status, 'p')
        self.assertEqual(Basket.objects.filter(user=self.user).count(), 0)
