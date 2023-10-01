from product.models import ProductImage, ProductCategory, Tag, Reviews, Product, Basket
from user.models import User

from django.test import TestCase


class TestCaseModulOrder(TestCase):
    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(name="Category", description="Category Description",
                                                               href="category")
        self.tag = Tag.objects.create(title="Tag", href="tag")
        self.product = Product.objects.create(name="Product", title="Product Title", price=10.99)
        self.product.category.add(self.category)
        self.product.tags.add(self.tag)

    def test_exists_product_and_related_model(self):
        self.assertEqual(self.category.id, 1)
        self.assertEqual(self.tag.id, 1)
        self.assertEqual(self.product.id, 1)

    def test_product_category(self):
        self.assertEqual(self.product.category.count(), 1)
        self.assertEqual(self.product.category.first(), self.category)

    def test_product_tags(self):
        self.assertEqual(self.product.tags.count(), 1)
        self.assertEqual(self.product.tags.first(), self.tag)


class BasketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.product = Product.objects.create(name="Product", title="Product Title", description="Product Description",
                                              price=100.00, quantity=10)

    def test_basket_str(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=3)
        self.assertEqual(
            str(basket),
            f"Корзина для {self.user.username} | Продукт: {self.product.name}"
        )

    def test_basket_sum(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=3)
        self.assertEqual(basket.sum(), 300.0)

    def test_basket_de_json(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=3)
        basket_item = basket.de_json()
        self.assertEqual(
            basket_item,
            {
                'product_name': self.product.name,
                'quantity': 3,
                'price': float(self.product.price),
                'sum': 300.0,
            }
        )

    def test_basket_creation(self):
        basket, created = Basket.create_or_update(self.product.id, self.user)
        self.assertTrue(created)
        self.assertEqual(basket.user, self.user)
        self.assertEqual(basket.product, self.product)
        self.assertEqual(basket.quantity, 1)

    def test_basket_update(self):
        basket, created = Basket.create_or_update(self.product.id, self.user)
        self.assertTrue(created)
        initial_quantity = basket.quantity
        basket, created = Basket.create_or_update(self.product.id, self.user)
        self.assertFalse(created)
        self.assertEqual(basket.quantity, initial_quantity + 1)


class ReviewsModelTestCase(TestCase):
    def setUp(self):
        self.review = Reviews.objects.create(
            author="Test Author",
            email="test@example.com",
            rate=4.5,
            text="Test Review",
        )

    def test_reviews_str(self):
        self.assertEqual(str(self.review), "Test Author")

