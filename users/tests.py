from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user
from .models import CustomUser
# Create your tests here.


class RegistrationTestCase(TestCase):
    def test_user_is_created(self):
        

        response = self.client.post(
            reverse('users:register'), 
            data={
                'username': 'jahongir22', 
                'first_name': 'Jahongir', 
                'last_name': 'Rakhmonov',
                'email': 'jrakhmonov@gmail.com',
                'password': 'somepassword',
                'confirm_password': 'somepassword'
                
                }
            )
       
        user = CustomUser.objects.get(username='jahongir22')

        
        self.assertEqual(user.first_name, 'Jahongir')
        self.assertEqual(user.last_name, 'Rakhmonov')
        self.assertEqual(user.email, 'jrakhmonov@gmail.com')
        
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))
        

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Jahongir',
                'email': 'jahongir2@gamil.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", 'username', 'This field is required.')
        self.assertFormError(response, "form", 'password', 'This field is required.')
        

    def test_invalid_email(self):
            response = self.client.post(
            reverse('users:register'), 
            data={
                'username': 'jahongir', 
                'first_name': 'Jahongir', 
                'last_name': 'Rakhmonov',
                'email': 'invalid-email',
                'password': 'somepassword'
                
                }
            )
            user_count = CustomUser.objects.count()

            self.assertEqual(user_count, 0)
            self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir')
        user.set_password("somepassword")
        user.save()
        

        response2 = self.client.post(
            reverse('users:register'), 
            data={
                'username': 'jahongir', 
                'first_name': 'Jahongir2', 
                'last_name': 'Rakhmonov2',
                'email': 'jahongir2@gmail.com',
                'password': 'somepassword2'
                
                }
            )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response2, 'form', 'username', 'A user with that username already exists.')

class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='jahongir', first_name='Jakhongir')
        self.db_user.set_password('somepassword')
        self.db_user.save()

    def test_successful_login(self):
       


        self.client.post(
            reverse('users:login'),
            data={
                'username': 'jahongir',
                'password': 'somepassword'
            }
        ) 

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)    

    def test_wrong_credentials(self):

       


        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong-username',
                'password': 'somepassword'
            }
        ) 

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse('users:login'),
            data={
                'username': 'jahongir',
                'password': 'wrong-pass'
            }
        ) 

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
       


        self.client.login(username='jahongir', password='Jsomepassword')

        self.client.get(reverse('users:logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))


        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')


    def test_profile_details(self):
        user = CustomUser.objects.create(username='polat', first_name = 'Polat', last_name='Alemdar',
                                    email="polat@gmal.com")
        user.set_password('somepassword')
        user.save()

        self.client.login(username='polat', password='somepassword')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username='polat', first_name = 'Polat', last_name='Alemdar',
                                    email="polat@gmal.com")
        user.set_password('somepassword')
        user.save()

        self.client.login(username='polat', password="somepassword")

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'polat',
                'first_name': 'pakalat',
                'last_name': 'salemdar',
                'email': 'polatjon@gmail.com'
            }
        )
        # user1 = User.objects.get(pk=user.pk) # pastdagi kod bilan bir xil vazifani bajaradi
        user.refresh_from_db()

        self.assertEqual(user.first_name, 'pakalat')
        self.assertEqual(user.last_name, 'salemdar')
        self.assertEqual(user.email, 'polatjon@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))



