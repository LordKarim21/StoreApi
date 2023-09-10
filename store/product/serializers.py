from rest_framework import fields, serializers

from models import Basket, Product, ProductCategory, Reviews, Tag, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCategory model.
    """
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Reviews model.
    """
    class Meta:
        model = Reviews
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    image = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = '__all__'
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
