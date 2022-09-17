'''
Test cases for comments
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Album
from .models import Comment


class CommentListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')

    def test_can_list_comments(self):
        '''
        View all comments
        '''
        admin = User.objects.get(username='admin')
        album = Album.objects.create(owner=admin, title='Album 1')
        Comment.objects.create(owner=admin, album=album, content='comment')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        '''
        Create Comment with logged in user
        '''
        self.client.login(username='admin', password='pass')
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post(
            '/comments/', {'album': 1, 'content': 'a content'})
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_comment(self):
        '''
        Create comment with logged out user
        '''
        admin = User.objects.get(username='admin')
        Album.objects.create(owner=admin, title='Album 1')
        response = self.client.post(
            '/comments/', {'album': 1, 'content': 'a content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    '''
    Test individual comment
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        user1 = User.objects.create_user(username='user1', password='pass')
        album1 = Album.objects.create(owner=admin, title='admin album')
        Comment.objects.create(
            owner=admin, album=album1, content='admin comment')
        album2 = Album.objects.create(owner=user1, title='user1 album')
        Comment.objects.create(
            owner=user1, album=album2, content='user1 comment')

    def test_can_retrieve_comment_using_valid_id(self):
        '''
        Fetch comment with valid id
        '''
        response = self.client.get('/comments/1')
        self.assertEqual(response.data['content'], 'admin comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_comment_using_invalid_id(self):
        '''
        Fetch comment with invalid id
        '''
        response = self.client.get('/comments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        '''
        Edit own comment
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/comments/1', {'content': 'a new comment'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'a new comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_user_comment(self):
        '''
        Edit another user's comment
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/comments/2', {'content': 'a new comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_comment(self):
        '''
        Edit comment without login
        '''
        response = self.client.put('/comments/1', {'content': 'a new comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
