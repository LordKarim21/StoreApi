from django.contrib import admin
from .models import Tag, Basket, Product, \
    ProductCategory, ProductImage, Reviews


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'href']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',)
    fields = ('image', 'name', 'description', ('price', 'quantity'),
              'stripe_product_price_id', 'category', 'reviews', 'tags')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'href']


@admin.register(ProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'email', 'rate']
