from django.db import models
from product.models import Basket
from user.models import User


class Order(models.Model):
    """
    Represents an order made by a user.
    """
    STATUS_CHOICES = [
        ('p', 'Подтвержден'),
        ('o', 'Не подтвержден'),
        ('n', 'Отменен')
    ]
    TYPE_DELIVERY = [
        ('o', 'Обычная доставка'),
        ('e', 'Экспресс доставка')
    ]
    TYPE_PAYMENT = [
        ('o', 'Онлайн картой'),
        ('r', 'Онлайн со случайного чужого счета')
    ]
    basket_history = models.JSONField(default=dict)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=256, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)

    city = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)

    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    type_delivery = models.CharField(max_length=1, choices=TYPE_DELIVERY, default='o')
    type_payment = models.CharField(max_length=1, choices=TYPE_PAYMENT, default='o')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='o')

    quantity = models.PositiveIntegerField(default=0)
    payment_error = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = 'p'
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
