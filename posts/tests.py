from django.test import TestCase
from django.test import Client
from .models import User


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="sarah", email="connor.s@skynet.com", password="12345")
    

    def test_profile(self): #проверка на создание персональной страницы   
        response = self.client.get("/sarah/")
        self.assertEqual(response.status_code, 200)
        

    def test_new(self):
        self.auth_user = {'username':self.user.username, 'password1':self.user.password, 'password2':self.user.password, 'email':self.user.email}
        self.client.login(username='sarah', password='12345')
        response = self.client.get("/new/")    
        self.assertEqual(response.status_code, 200) #авторизованный пользователь может опубликовать пост
        self.client.post('/new/', {'text' : "FirstPost"}) #проверка на публикацию поста
        response = self.client.get('/') 
        self.assertContains(response, text='FirstPost', status_code=200)
        response = self.client.get("/sarah/")
        self.assertContains(response, text='FirstPost', status_code=200)
        response = self.client.get("/sarah/1/")
        self.assertContains(response, text='FirstPost', status_code=200)                
        response = self.client.post('/sarah/1/edit', {'text' : "EditPost"}, follow=True) #проверка на изменение поста
        response = self.client.get('/') 
        self.assertContains(response, text='EditPost', status_code=200)
        response = self.client.get("/sarah/")
        self.assertContains(response, text='EditPost', status_code=200)
        response = self.client.get("/sarah/1/")
        self.assertContains(response, text='EditPost', status_code=200)


class test_not_auth(TestCase): #Неавторизованный посетитель не может опубликовать пост
    def setUp(self):
        self.client = Client()


    def test_redirect(self):
        response = self.client.get('/new/')
        self.assertRedirects(response, '/')
