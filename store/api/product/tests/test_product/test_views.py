from user.models import User
from product.models import Product, ProductCategory, Tag, Reviews, ProductImage, Basket

from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse_lazy


class ProductViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = ProductCategory.objects.create(name="Test Category", href="test-category")
        self.tag = Tag.objects.create(title="Test Tag", href="test-tag")
        self.product = Product.objects.create(
            name="Test Product",
            title="Test Product Title",
            price=100.0,
            quantity=10,
        )
        self.product.category.add(self.category)
        self.product.tags.add(self.tag)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=3)
        self.client.login(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_product_detail_view(self):
        response = self.client.get(reverse_lazy("product:products-detail", args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Product")

    # def test_get_catalog(self):
    #     url = reverse_lazy('product:catalog-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class BasketViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = ProductCategory.objects.create(name="Test Category", href="test-category")
        self.tag = Tag.objects.create(title="Test Tag", href="test-tag")
        self.product = Product.objects.create(
            name="Test Product",
            title="Test Product Title",
            price=100.0,
            quantity=10,
        )
        self.product.category.add(self.category)
        self.product.tags.add(self.tag)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=3)
        self.client.login(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_remove_from_basket_view(self):
        with self.assertRaises(KeyError):
            response = self.client.post(reverse_lazy("product:basket-remove", kwargs={"basket_id": self.basket.id}))
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_add_to_basket_view(self):
        with self.assertRaises(KeyError):
            response = self.client.post(reverse_lazy("product:basket-add", kwargs={"product_id": self.product.id}))
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_basket_view(self):
        response = self.client.get(reverse_lazy("product:basket-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Product")
