from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = "order"

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'orders/active', views.active, name='active')
]
