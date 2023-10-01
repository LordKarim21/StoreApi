from . import serializers
from . import models
from product.models import Basket

from django.http import HttpResponseRedirect
from http import HTTPStatus

from rest_framework.response import Response
import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing orders.
    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)

    def create(self, request, *args, **kwargs):
        object = super().create(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': object.data['id']},
            mode='payment',
            success_url='http://127.0.0.1:8000/',
            cancel_url='http://127.0.0.1:8000/',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def active(request):
    queryset = models.Order.objects.filter(initiator=request.user).filter(status='o')
    if queryset.exists():
        serializer = serializers.OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': "Not exists active Order"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        fulfill_order(session)

    return HttpResponse(status=status.HTTP_200_OK)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
