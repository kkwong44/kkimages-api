'''
Test cases for likes
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Album
from .models import Like


class LikeListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')

    def test_can_list_likes(self):
        '''
        View all likes without logged in
        '''
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_like(self):
        '''
        Like album with logged in user
        '''
        self.client.login(username='admin', password='pass')
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post('/likes/', {'album': 1})
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_like(self):
        '''
        Like album with logged out user
        '''
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post('/likes/', {'album': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    '''
    Test individual like
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        user1 = User.objects.create_user(username='user1', password='pass')
        album1 = Album.objects.create(owner=admin, title='admin title')
        Like.objects.create(owner=admin, album=album1)
        album2 = Album.objects.create(owner=user1, title='user1 title')
        Like.objects.create(owner=user1, album=album2)

    def test_can_retrieve_like_using_valid_id(self):
        '''
        Fetch like with valid id
        '''
        response = self.client.get('/likes/1')
        self.assertEqual(response.data['album'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_like_using_invalid_id(self):
        '''
        Fetch like with invalid id
        '''
        response = self.client.get('/likes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_like(self):
        '''
        Unlike album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/likes/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_like(self):
        '''
        Unlike another user's like to an album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/likes/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_delete_like(self):
        '''
        Unlike album while logged out
        '''
        response = self.client.delete('/likes/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
