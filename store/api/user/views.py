from . import serializers
from . import models
from .tasks import send_email_verification

from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    View to log the user out.
    """
    django_logout(request)
    return Response({'message': 'Вы успешно вышли из системы'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def login(request):
    """
    View to log the user in.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            django_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Пользователь неактивен'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неверное имя пользователя или пароль'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    email = request.data.get('email')

    if password1 != password2:
        return Response({'error': 'Два поля пароля не совпадали.'},
                        status=status.HTTP_400_BAD_REQUEST)
    password = password2
    if not username or not password:
        return Response({'error': 'Поле "username" и "password" обязательны для заполнения'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    user = models.User.objects.create_user(
        username=username, password=password, email=email, first_name=first_name, last_name=last_name
    )
    send_email_verification.delay(user.id)

    django_login(request, user)

    return Response({'message': 'Регистрация прошла успешно', 'user_id': user.id}, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'error': 'Старый пароль указан неверно'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)

    return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_avatar(request):
    user = request.user
    avatar = request.data.get('avatar')

    if avatar is not None:
        user.avatar = avatar
        user.save()
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Не удалось обновить изображение пользователя'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify(request, user_id, email, code):
    user = models.User.objects.get(id=user_id)
    if user.email == email:
        verification = models.EmailVerification.objects.filter(code=code, user=user)
        if verification.exists() and not verification.first().is_expired():
            user.is_verification_email = True
            user.save()

            verification.delete()
            return Response({'message': 'Email успешно подтвержден'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код верификации или код устарел'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неверный email'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing payment information.
    """
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    permission_classes = (IsAuthenticated, )


class AccountViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing user data.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing user model.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )
