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

router.register('catalog', views.CatalogListAPIView, basename='catalog')

router.register(r'basket', views.BasketModelViewSet, basename='basket')

urlpatterns = [
    path('', include(router.urls)),
    path(r'basket/add/<int:product_id>/', views.BasketModelViewSet.as_view({'post': 'basket_add'}), name='basket-add'),
    path(r'basket/remove/<int:basket_id>/', views.BasketModelViewSet.as_view({'post': 'basket_remove'}),
         name='basket-remove'),
    path(r'products/<int:product_id>/reviews', views.ProductViewSet.as_view(
        {'post': 'reviews_create'}), name='reviews-create'),
    path(r'products/<int:product_id>/reviews', views.ProductViewSet.as_view(
        {'get': 'reviews_list'}), name='reviews-list'),
]
