'''
Test cases for albums
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from photos.models import Photo
from comments.models import Comment
from likes.models import Like
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

    def test_can_list_albums(self):
        '''
        All users can view all albums
        '''
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='a title', cover_image='cover')
        response = self.client.get('/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_album(self):
        '''
        Logged in user can create albums with default image
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.post(
            '/albums/', {'title': 'a title', 'skill_level': 'Other'})
        count = Album.objects.count()
        self.assertEqual(count, 1)
        album = Album.objects.filter(pk=1).first()
        self.assertEqual(album.cover_image, '../default_post_liudmg')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_can_create_album_with_upload_image(self):
        '''
        Logged in user can create albums with upload image
        '''
        self.client.login(username='admin', password='pass')
        admin = User.objects.get(username='admin')
        album = Album.objects.create(
            owner=admin, title='a title', content='admin content',
            cover_image='UploadImage')
        count = Album.objects.count()
        self.assertEqual(count, 1)
        album = Album.objects.filter(pk=1).first()
        self.assertEqual(album.cover_image, 'UploadImage')

    def test_logged_out_user_cant_create_album(self):
        '''
        Not allow to create album while logged out
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
        album1 = Album.objects.create(
            owner=admin, title='a title', content='admin content',
            skill_level='Other')
        album2 = Album.objects.create(
            owner=user1, title='a title', content='user1 content',
            skill_level='Other')
        # Album's children items
        Photo.objects.create(owner=admin, album=album1, title='photo 1')
        Photo.objects.create(owner=admin, album=album1, title='photo 2')
        Photo.objects.create(owner=admin, album=album2, title='photo 1')
        Comment.objects.create(owner=admin, album=album1, content='comment 1')
        Comment.objects.create(owner=admin, album=album1, content='comment 2')
        Comment.objects.create(owner=admin, album=album2, content='comment 1')
        Like.objects.create(owner=admin, album=album1)
        Like.objects.create(owner=user1, album=album1)

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
        response = self.client.put(
            '/albums/1', {'title': 'a new title', 'skill_level': 'Other'})
        album = Album.objects.filter(pk=1).first()
        self.assertEqual(album.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_album(self):
        '''
        Not allow to edit another user's album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/albums/2', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_album(self):
        '''
        Not allow to edit album without logged in
        '''
        response = self.client.put('/albums/1', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_album(self):
        '''
        Delete own album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/albums/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_album(self):
        '''
        Not allow to delete other user's album
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/albums/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_delete_album(self):
        '''
        Not allow to delete album without logged in
        '''
        response = self.client.delete('/albums/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_album_and_contents(self):
        '''
        Delete own album and all children
        '''
        self.client.login(username='admin', password='pass')
        count = Photo.objects.count()
        self.assertEqual(count, 3)
        count = Comment.objects.count()
        self.assertEqual(count, 3)
        count = Like.objects.count()
        self.assertEqual(count, 2)
        response = self.client.delete('/albums/1')
        count = Photo.objects.count()
        self.assertEqual(count, 1)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        count = Like.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
