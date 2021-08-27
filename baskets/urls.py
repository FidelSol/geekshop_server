from django.urls import path

from baskets.views import basket_add, basket_remove, basket_edit

app_name = 'baskets'

urlpatterns = [
    path('add/', basket_add, name='basket_add'),
    path('remove/<int:id>/', basket_remove, name='basket_remove'),
    path('edit/', basket_edit, name='basket_edit'),
]