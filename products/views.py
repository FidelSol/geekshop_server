from django.shortcuts import render


# index
def index(request):
    return render(request, 'index.html')

# contact
def contact(request):
    return render(request, 'contact.html')

# index
def products(request):
    return render(request, 'products.html')