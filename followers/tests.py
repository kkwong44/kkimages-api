'''
Test cases for followers
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Follower


class FollowerListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')
        User.objects.create_user(username='user1', password='pass')

    def test_can_list_followers(self):
        '''
        View all followers without logged in
        '''
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_follow(self):
        '''
        Logged in user follow another user
        '''
        self.client.login(username='admin', password='pass')
        User.objects.get(username='admin')
        response = self.client.post('/followers/', {'followed': 2})
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_can_follow_multiple(self):
        '''
        Logged in user follow multiple users
        '''
        self.client.login(username='admin', password='pass')
        User.objects.get(username='admin')
        response = self.client.post('/followers/', {'followed': 1})
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/followers/', {'followed': 2})
        count = Follower.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class FollowerDetailViewTests(APITestCase):
    '''
    Test individual follower
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        Follower.objects.create(owner=admin, followed=user1)
        Follower.objects.create(owner=admin, followed=user2)

    def test_can_retrieve_followers_using_valid_id(self):
        '''
        Fetch number of followers with valid id
        '''
        response = self.client.get('/followers/1')
        self.assertEqual(response.data['followed'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_followers_using_invalid_id(self):
        '''
        Fetch number of followers with an invalid id
        '''
        response = self.client.get('/followers/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_unfollow_users(self):
        '''
        Unfollow followed user
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/followers/1')
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_unfollow_another_user_followers(self):
        '''
        Unfollow another user's followers
        '''
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/followers/1')
        count = Follower.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_unfollow_user(self):
        '''
        Unfollow user while logged out
        '''
        response = self.client.delete('/followers/1')
        count = Follower.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
