from django.test import TestCase
from django.test import Client
from .forms import User


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="sarah", email="connor.s@skynet.com", password="12345")
    

    def test_profile(self): #проверка на создание персональной страницы   
        response = self.client.post('/auth/singup/', {'first_name': "EditPost", 'last_name': 'sss', 'username': 'lox', 'email': 'wolf.alex111@mail.ru'}, follow=True)
        response = self.client.get('/singup')
        
