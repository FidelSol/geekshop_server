from django.conf import settings
from django.test import TestCase

from django.test import TestCase
from django.test.client import Client
from products.models import Product, ProductCategory
from django.core.management import call_command

from users.models import User


class TestMainappSmoke(TestCase):
   def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

   def test_mainapp_urls(self):
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/contact/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/category/0/')
       self.assertEqual(response.status_code, 200)

       for category in ProductCategory.objects.all():
           response = self.client.get(f'/products/category/{category.pk}/')
           self.assertEqual(response.status_code, 200)

       for product in Product.objects.all():
           response = self.client.get(f'/products/product/{product.pk}/')
           self.assertEqual(response.status_code, 200)

   def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'baskets')


class TestUserManagement(TestCase):
   def setUp(self):
       call_command('flush', '--noinput')
       call_command('loaddata', 'test_db.json')
       self.client = Client()

       self.superuser = User.objects.create_superuser('django', 'django@geekshop.local', '1234')

       self.user = User.objects.create_user('gonza', 'gonza@geekshop.local', '1234')

       self.user_with__first_name = User.objects.create_user('fidel', 'fidel@geekshop.local', '1234', first_name='Fidel')

   def test_user_login(self):
       # главная без логина
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)
       self.assertTrue(response.context['user'].is_anonymous)
       self.assertEqual(response.context['title'], 'главная')
       self.assertNotContains(response, 'Пользователь', status_code=200)
       # self.assertNotIn('Пользователь', response.content.decode())

       # данные пользователя
       self.client.login(username='tarantino', password='geekbrains')

       # логинимся
       response = self.client.get('/auth/login/')
       self.assertFalse(response.context['user'].is_anonymous)
       self.assertEqual(response.context['user'], self.user)

       # главная после логина
       response = self.client.get('/')
       self.assertContains(response, 'Пользователь', status_code=200)
       self.assertEqual(response.context['user'], self.user)
       # self.assertIn('Пользователь', response.content.decode())

   def test_user_logout(self):
       # данные пользователя
       self.client.login(username='gonza', password='1234')

       # логинимся
       response = self.client.get('/users/login/')
       self.assertEqual(response.status_code, 200)
       self.assertFalse(response.context['user'].is_anonymous)

       # выходим из системы
       response = self.client.get('/users/logout/')
       self.assertEqual(response.status_code, 302)

       # главная после выхода
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)
       self.assertTrue(response.context['user'].is_anonymous)

   def test_user_register(self):
       # логин без данных пользователя
       response = self.client.get('/users/register/')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.context['title'], 'регистрация')
       self.assertTrue(response.context['user'].is_anonymous)

       new_user_data = {
           'username': 'samuel',
           'first_name': 'Сэмюэл',
           'last_name': 'Джексон',
           'password1': 'geekbrains',
           'password2': 'geekbrains',
           'email': 'sumuel@geekshop.local',
           'age': '21'}

       response = self.client.post('/users/register/', data=new_user_data)
       self.assertEqual(response.status_code, 302)

       new_user = User.objects.get(username=new_user_data['username'])

       activation_url = f"{settings.DOMAIN_NAME}/users/verify/{new_user_data['email']}/{new_user.activation_key}/"

       response = self.client.get(activation_url)
       self.assertEqual(response.status_code, 200)

       # данные нового пользователя
       self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

       # логинимся
       response = self.client.get('/users/login/')
       self.assertEqual(response.status_code, 200)
       self.assertFalse(response.context['user'].is_anonymous)

       # проверяем главную страницу
       response = self.client.get('/')
       self.assertContains(response, text=new_user_data['first_name'], status_code=200)

   def test_user_wrong_register(self):
       new_user_data = {
           'username': 'teen',
           'first_name': 'Мэри',
           'last_name': 'Поппинс',
           'password1': 'geekbrains',
           'password2': 'geekbrains',
           'email': 'merypoppins@geekshop.local',
           'age': '17'}

       response = self.client.post('/users/register/', data=new_user_data)
       self.assertEqual(response.status_code, 200)
       self.assertFormError(response, 'UserRegistrationForm', 'age', 'Вы слишком молоды!')

   def tearDown(self):
       call_command('sqlsequencereset', 'products', 'users', 'orders', 'baskets')



