from django.db import connection
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from admins.views import db_profile_by_type
from products.models import ProductCategory
from users.forms import UserRegistrationForm, UserProfileForm
from django import forms

from users.models import User


class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class ProductCategoryEditForm(forms.ModelForm):
   discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

   class Meta:
       model = ProductCategory
       exclude = ()

class ProductCategoryUpdateView(UpdateView):
   model = ProductCategory
   template_name = 'adminapp/category_update.html'
   success_url = reverse_lazy('admin:categories')
   form_class = ProductCategoryEditForm

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['title'] = 'категории/редактирование'
       return context

   def form_valid(self, form):
       if 'discount' in form.cleaned_data:
           discount = form.cleaned_data['discount']
           if discount:
               self.object.product_set.\
                    update(price=F('price') * (1 - discount / 100))
               db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

       return super().form_valid(form)



