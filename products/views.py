import json
from urllib.request import urlopen

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse

from products.models import ProductCategory, Product


# index
@login_required
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)

# contact
@login_required
def contact(request):
    context = {'title': 'GeekShop - Контакты'}
    return render(request, 'products/contact.html', context)

# index
@login_required
def products(request):
    catedories = ProductCategory.objects.all()
    products = Product.objects.all()
    context = {'title': 'GeekShop - Продукты', 'categories': catedories, 'products': products}
    return render(request, 'products/products.html', context)