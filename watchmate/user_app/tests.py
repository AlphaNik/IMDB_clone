from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token



class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "testuser",
            "password2": "testuser"
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.data['username'],data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_register_with_mismatched_passsword(self):
        pass

    def test_register_with_mission_data(self):
        pass


class LoginLogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', 
                                             email='testuser@gmail.com', 
                                             password='testuser')
        
    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testuser"
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        response = self.client.post(reverse('logout'))
        #print(f'response is : {response} |data is :{response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        




