from django.db import models
from django.conf import settings
from user.models import User
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductImage(models.Model):
    """
    Represents an image associated with a product.
    """
    image = models.ImageField(upload_to="products_images")


class ProductCategory(models.Model):
    """
    Represents a category that a product can belong to.
    """
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    href = models.SlugField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag that can be associated with a product.
    """
    title = models.CharField(max_length=128)
    href = models.SlugField()

    def __str__(self):
        return self.title


class Reviews(models.Model):
    """
    Represents a review for a product.
    """
    author = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    text = models.TextField()
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.author


class Product(models.Model):
    """
    Represents a product available for sale.
    """
    TYPE_DELIVERY = [
        ('f', 'Бесплатная'),
        ('p', 'Платная')
    ]
    delivery = models.CharField(max_length=1, choices=TYPE_DELIVERY, default='p')

    name = models.CharField(max_length=256)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    image = models.ManyToManyField(ProductImage)
    reviews = models.ManyToManyField(Reviews, related_name='reviews')
    tags = models.ManyToManyField(Tag)
    category = models.ManyToManyField(ProductCategory)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        if not line_items:
            item = {
                'price': 'price_1Nop4EJbf2DfQ8pKXcphqESb',
                'quantity': 1,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_crated = False
            return basket, is_crated
