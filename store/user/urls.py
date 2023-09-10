from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "user"

router = DefaultRouter()
router.register(r'account', views.AccountViewSet, basename="account")
router.register(r'payment', views.PaymentViewSet, basename='payment')
router.register(r'profile', views.UserViewSet, basename='profile')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'sign-out/', views.logout, name='logout'),
    path(r'sign-up/', views.register, name='createauth'),
    path(r'sign-in/', views.login, name='login'),
    path(r'profile/<int:pk>/verify/<str:email>/<uuid:code>/', views.verify, name='verify'),
    path(r'profile/<int:pk>/password', views.change_password, name='password'),
    path(r'profile/<int:pk>/avatar', views.change_avatar, name='avatar'),
]
