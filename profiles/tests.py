'''
Test cases for profiles
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')
        User.objects.create_user(username='user1', password='pass')

    def test_can_list_profiles(self):
        '''
        View all profiles without logged in
        '''
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_out_user_can_login(self):
        '''
        Log in
        '''
        response = self.client.login(username='admin', password='pass')
        self.assertEqual(response, True)

    def test_inavalid_login(self):
        '''
        Invalid login
        '''
        response = self.client.login(username='adminxxx', password='pass')
        self.assertEqual(response, False)
        response = self.client.login(username='admin', password='passxxx')
        self.assertEqual(response, False)
        response = self.client.login(username='adminxxx', password='passxxx')
        self.assertEqual(response, False)


class ProfileDetailViewTests(APITestCase):
    '''
    Test individual Profile
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        User.objects.create_user(username='admin', password='pass')
        User.objects.create_user(username='user1', password='pass')

    def test_can_retrieve_profile_using_valid_id(self):
        '''
        Fetch profile with valid id
        '''
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_profile_using_invalid_id(self):
        '''
        Fetch profile with invalid id
        '''
        response = self.client.get('/profiles/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profile(self):
        '''
        Edit own profile
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/profiles/1/', {'content': 'a new title'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.content, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_user_profile(self):
        '''
        Edit other user profile
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/profiles/2/', {'content': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_profile(self):
        '''
        Edit other user profile with logged out
        '''
        response = self.client.put('/profiles/1/', {'content': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_profile(self):
        '''
        Delete own profile
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_profile(self):
        '''
        Not allow to delete other user's profile
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/profiles/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_delete_profile(self):
        '''
        Not allow to delete profile without logged in
        '''
        response = self.client.delete('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
