import json
from urllib.request import urlopen
from django.shortcuts import render
from django.apps import apps

# index
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'index.html', context)

# contact
def contact(request):
    context = {'title': 'GeekShop - Контакты'}
    return render(request, 'contact.html', context)

# index
def products(request):
    context = {'title': 'GeekShop - Продукты'}
    path = apps.get_app_config('products').path
    with open(path + '\\fixtures\\products.json', 'r', encoding='UTF8') as f:
        context = json.load(f)
    print(context)
    return render(request, 'products.html', context)