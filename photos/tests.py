'''
Test cases for photos
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Album
from .models import Photo


class PhotoListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')

    def test_can_list_photos(self):
        '''
        All user can view all photos
        '''
        admin = User.objects.get(username='admin')
        album = Album.objects.create(owner=admin, title='Album 1')
        Photo.objects.create(owner=admin, album=album, title='photo')
        response = self.client.get('/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_photo(self):
        '''
        Logged in user can create own album photos
        '''
        self.client.login(username='admin', password='pass')
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post(
            '/photos/', {'album': 1, 'title': 'a title'})
        count = Photo.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_photo(self):
        '''
        Logged out user can't create photos
        '''
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post(
            '/photos/', {'album': 1, 'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PhotoDetailViewTests(APITestCase):
    '''
    Test individual photo
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        user1 = User.objects.create_user(username='user1', password='pass')
        album1 = Album.objects.create(owner=admin, title='admin title')
        Photo.objects.create(owner=admin, album=album1, title='admin photo')
        album2 = Album.objects.create(owner=user1, title='user1 title')
        Photo.objects.create(owner=user1, album=album2, title='user1 photo')

    def test_can_retrieve_photo_using_valid_id(self):
        '''
        Fetch photo with valid id
        '''
        response = self.client.get('/photos/1')
        self.assertEqual(response.data['title'], 'admin photo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_photo_using_invalid_id(self):
        '''
        Fetch photo with invalid id
        '''
        response = self.client.get('/photos/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_photo(self):
        '''
        Edit own photo
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/photos/1', {'title': 'a new photo'})
        photo = Photo.objects.filter(pk=1).first()
        self.assertEqual(photo.title, 'a new photo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_photo(self):
        '''
        Not allow to edit another user's photo
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/photos/2', {'title': 'a new photo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_photo(self):
        '''
        Not allow to edit photo without login
        '''
        response = self.client.put('/photos/1', {'title': 'a new photo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_photo(self):
        '''
        Delete own photo
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/photos/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_photo(self):
        '''
        Not allow to delete other user's photo
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/photos/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_delete_photo(self):
        '''
        Not allow to delete photo without logged in
        '''
        response = self.client.delete('/photos/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
