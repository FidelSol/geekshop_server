import json
from urllib.request import urlopen
from django.shortcuts import render
from django.apps import apps

# index
from products.models import ProductCategory, Product


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'index.html', context)

# contact
def contact(request):
    context = {'title': 'GeekShop - Контакты'}
    return render(request, 'contact.html', context)

# index
def products(request):
    catedories = ProductCategory.objects.all()
    products = Product.objects.all()
    context = {'title': 'GeekShop - Продукты', "categories": catedories, "products": products}
    return render(request, 'products.html', context)