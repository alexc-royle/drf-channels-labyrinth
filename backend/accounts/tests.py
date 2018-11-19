from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'test@example.com', 'testpassword')
        self.create_url = reverse('account-create')
        self.authenticate_url = reverse('account-gettoken')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is associated with itself.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'foo'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Ensure user is not created with no password.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        """
        Ensure user is not created with a ridiculously long username
        """
        data = {
            'username': 'foo'*11,
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        """
        Ensure user is not created without a username
        """
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        """
        Ensure user is not created if a user with the same username already exists
        """
        data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        """
        Ensure user is not created if a user with the same email already exists
        """
        data = {
            'username': 'test_user2',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        """
        Ensure user is not created with an invalid email
        """
        data = data = {
            'username': 'foobar',
            'email': 'testing',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        """
        Ensure user is not created without an email
        """
        data = data = {
            'username': 'foobar',
            'email': '',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)


    def test_authenticate_user(self):
        """
        Ensure we can authenticate a user and get a valid token in return.
        """
        data = {
            'username': 'test_user',
            'password': 'testpassword'
        }
        response = self.client.post(self.authenticate_url, data, format='json')
        user = User.objects.get(username=data['username'])
        token = Token.objects.get(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], user.id)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], user.email)
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['token'], token.key)

    def test_authenticate_user_with_no_username(self):
        """
        Ensure we cannot authenticate a user if we are given a blank username
        """
        data = {
            'username': '',
            'password': 'testpassword'
        }
        response = self.client.post(self.authenticate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['username']), 1)

    def test_authenticate_user_with_no_password(self):
        """
        Ensure we cannot authenticate a user if we are given a blank password
        """
        data = {
            'username': 'test_user',
            'password': ''
        }
        response = self.client.post(self.authenticate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_authenticate_user_with_incorrect_username(self):
        """
        Ensure we cannot authenticate a user if we are given an incorrect username
        """
        data = {
            'username': 'test_user_2',
            'password': 'testpassword'
        }
        response = self.client.post(self.authenticate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)

    def test_authenticate_user_with_incorrect_password(self):
        """
        Ensure we cannot authenticate a user if we are given an incorrect username
        """
        data = {
            'username': 'test_user',
            'password': 'testpassword_2'
        }
        response = self.client.post(self.authenticate_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)
