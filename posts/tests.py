from django.test import TestCase
from django.test import Client
from .models import User
from . import views
from django.urls import reverse


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="sarah", email="connor.s@skynet.com", password="12345")
    
    def test_profile(self):  # проверка на создание персональной страницы   
        response = self.client.post('/auth/signup/', {'first_name': "Alexey", 
                                    'last_name': 'Volkov', 'username': 'AGV', 'email': 'volkov@mail.ru', 
                                    "password1": "123qwe12", 'password2': '123qwe12'}, follow=True)
        response = self.client.get("/AGV/")
        self.assertEqual(response.status_code, 200)        

    def test_new(self):
        self.client.login(username='sarah', password='12345')  
        response = self.client.post(reverse('new_post'), {'text': 'FirstPost'}, follow=True)  # авторизованный пользователь может опубликовать пост
        response = self.client.get('/')  # проверка на публикацию поста
        self.assertContains(response, text='FirstPost', status_code=200)
        response = self.client.get("/sarah/")
        self.assertContains(response, text='FirstPost', status_code=200)
        response = self.client.get("/sarah/1/")
        self.assertContains(response, text='FirstPost', status_code=200)                              
        
    def test_edit(self):    
        self.client.login(username='sarah', password='12345')
        response = self.client.post(reverse('new_post'), {'text': 'FirstPost'}, follow=True)
        response = self.client.post(reverse('post_edit', kwargs={'username': 'sarah', 'post_id': '1'}),
                                           {'text': 'EditPost'}, follow=True)  # проверка на изменение поста
        response = self.client.get('/') 
        self.assertContains(response, text='EditPost', status_code=200)
        response = self.client.get("/sarah/")
        self.assertContains(response, text='EditPost', status_code=200)
        response = self.client.get("/sarah/1/")
        self.assertContains(response, text='EditPost', status_code=200)


class test_not_auth(TestCase):  # Неавторизованный посетитель не может опубликовать пост
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        response = self.client.get('/new/')
        self.assertRedirects(response, '/')
