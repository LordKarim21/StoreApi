from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now
from django.conf import settings


class Payment(models.Model):
    """
    Represents a payment method for users.
    """
    number_card = models.IntegerField(null=True, blank=True)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=25)


class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True, blank=True)
    is_verification_email = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_name)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подверждение учетной записи для {self.user.username}'
        message = 'Для подверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
