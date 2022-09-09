'''
Test cases for albums
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Album


class AlbumListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')

    def test_can_list_posts(self):
        '''
        View all albums
        '''
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='a title')
        response = self.client.get('/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_album(self):
        '''
        Create Album with logged in user
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.post('/albums/', {'title': 'a title'})
        count = Album.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_album(self):
        '''
        Create Album with logged out user
        '''
        response = self.client.post('/albums/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AlbumDetailViewTests(APITestCase):
    '''
    Test individual album
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        user1 = User.objects.create_user(username='user1', password='pass')
        Album.objects.create(
            owner=admin, title='a title', content='admin content')
        Album.objects.create(
            owner=user1, title='a title', content='user1 content')

    def test_can_retrieve_album_using_valid_id(self):
        '''
        Fetch album with valid id
        '''
        response = self.client.get('/albums/1')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_album_using_invalid_id(self):
        '''
        Fetch album with invalid id
        '''
        response = self.client.get('/albums/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_album(self):
        '''
        Edit own album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/albums/1', {'title': 'a new title'})
        album = Album.objects.filter(pk=1).first()
        self.assertEqual(album.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_album(self):
        '''
        Edit another user's album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/albums/2', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_album(self):
        '''
        Edit album without login
        '''
        response = self.client.put('/albums/1', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
