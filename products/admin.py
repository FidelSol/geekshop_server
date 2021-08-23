from django.contrib import admin
from products.models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'price', 'quantity', 'category')
    list_display_links = ('image', 'description', 'price', 'quantity', 'category')
    search_fields = ('description', 'price', 'quantity', 'category')