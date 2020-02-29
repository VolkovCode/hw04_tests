from django.test import TestCase

# Create your tests here.
def test_PostEdit(self):
        self.user = User.objects.create(
                username='testuser',
                email='test@email.com',
                password='testpassword'
                )
        self.client = Client()
        auth_user = {'username':self.user.username, 'password1':self.user.password, 'password2':self.user.password, 'email':self.user.email}
        self.client.post('/auth/signup/', auth_user, follow = True)
        auth_user = {'username':self.user.username, 'password':self.user.password}
        response = self.client.post('/auth/login/', auth_user)
        self.assertEqual(response.status_code, 200, msg = 'Не прошла авторизация')
        self.post = Post.objects.create(
            text='Test post',
            author=self.user,
            pub_date='01.01.2020'
            )
        modified_post = 'Modified new post'
        self.client.post(
            f'/{self.post.author}/{self.post.id}/edit/',
			{'text':self.user.password },
            follow=True
            )
        response = self.client.get('')
        self.assertContains(response, modified_post, status_code=200, msg_prefix='На главной нет изменений', html=False)