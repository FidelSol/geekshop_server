from django.urls import path

from buskets.views import basket_add, basket_remove

app_name = 'buskets'

urlpatterns = [
    path('add/<int:product_id>/', basket_add, name='basket_add'),
    path('remove/<int:id>/', basket_remove, name='basket_remove'),
]