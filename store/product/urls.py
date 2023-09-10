from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = "product"

router = DefaultRouter()
router.register("banners", views.BannersListAPIView, basename="banners")
router.register("products/limited", views.LimitedListAPIView, basename="limited")
router.register('products/popular', views.PopularListAPIView, basename='populars')

router.register('categories', views.CategoriesViewSet, basename='categories')
router.register('tags', views.TagViewSet, basename='tags')

router.register('products', views.ProductViewSet, basename='products')

router.register('catalog', views.CatalogListAPIView, basename='catalog_list')

router.register(r'basket', views.BasketModelViewSet, basename='basket')

urlpatterns = [
    path('', include(router.urls)),
    path(r'products/<int:pk>/reviews', views.reviews, name='reviews'),
]
