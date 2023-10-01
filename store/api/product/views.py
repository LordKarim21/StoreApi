from . import models
from . import serializers
from .paginator import StandardResultsSetPagination

from django.shortcuts import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class CatalogListAPIView(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["", ""]
    search_fields = ['title', 'description', ]

    def get_queryset(self):
        queryset = models.Product.objects.all()
        limit = self.request.GET.get('limit')
        sort = self.request.GET.get('sort')
        type_sort = self.request.GET.get('sortType')
        filter_name = self.request.GET.get(r'filter[name]')
        filter_min_price = self.request.GET.get(r'filter[minPrice]')
        filter_max_price = self.request.GET.get(r'filter[maxPrice]')
        filter_free_delivery = self.request.GET.get(r'filter[freeDelivery]')
        filter_available = self.request.GET.get(r'filter[available]')
        if filter_name:
            filter_name = filter_name.replace('+', ' ').strip()
            queryset = queryset.filter(Q(title__icontains=filter_name) & Q(description__icontains=filter_name))
        tags = []
        for tag in self.request.GET.getlist('tags[]'):
            tags.append(tag)
        if tags:
            try:
                queryset = queryset.filter(tags__id__in=tags)
            except ValueError:
                pass
        if filter_max_price and filter_min_price:
            queryset = queryset.filter(
                price__range=[filter_min_price, filter_max_price]
            )
        if filter_available == 'true':
            queryset = queryset.filter(quantity__lte=10)
        if filter_free_delivery == 'true':
            queryset = queryset.filter(delivery='f')
        else:
            queryset = queryset.filter(delivery='f')
        if sort == 'price':
            if type_sort == 'inc':
                queryset = queryset.order_by('price')
            elif type_sort == 'dec':
                queryset = queryset.order_by('-price')
        elif sort == 'rating':
            if type_sort == 'inc':
                queryset = queryset.order_by('rating')
            elif type_sort == 'dec':
                queryset = queryset.order_by('-rating')
        elif sort == 'date':
            if type_sort == 'inc':
                queryset = queryset.order_by('created')
            elif type_sort == 'dec':
                queryset = queryset.order_by('-created')
        elif sort == 'reviews':
            if type_sort == 'inc':
                queryset = queryset.order_by('reviews__rate')
            elif type_sort == 'dec':
                queryset = queryset.order_by('-reviews__rate')
        return queryset


class BannersListAPIView(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()[:3]
    serializer_class = serializers.ProductSerializer
    pagination_class = None


class LimitedListAPIView(viewsets.ModelViewSet):
    queryset = models.Product.objects.all().order_by('quantity')[:5]
    serializer_class = serializers.ProductSerializer
    pagination_class = None


class PopularListAPIView(viewsets.ModelViewSet):
    queryset = models.Product.objects.all().order_by('reviews')[:5]
    serializer_class = serializers.ProductSerializer
    pagination_class = None


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing product categories.
    """
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing product tags.
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ('create', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    @action(detail=False, methods=['POST'])
    def reviews_create(self, request, product_id):
        products = models.Product.objects.filter(id=product_id)
        if not products.exists():
            return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
        author = request.data.get('author')
        email = request.data.get('email')
        text = request.data.get('text')
        rate = request.data.get('rate')
        serializer = serializers.ReviewSerializer(
            author=author, email=email, text=text, rate=rate
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def reviews_list(self, product_id):
        products = models.Product.objects.filter(id=product_id)
        if not products.exists():
            return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
        reviews = product.review_set.all()
        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketModelViewSet(viewsets.ModelViewSet):
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = models.Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'The field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def basket_remove(self, request, basket_id):
        basket = models.Basket.objects.get(id=basket_id)
        basket.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    @action(detail=True, methods=['post'])
    def basket_add(self, request, product_id):
        models.Basket.create_or_update(product_id, request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
