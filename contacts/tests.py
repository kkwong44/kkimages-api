'''
Test cases for likes
'''
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Contact


class ContactListViewTests(APITestCase):
    '''
    Test List View
    '''
    def setUp(self):
        '''
        Setup user
        '''
        User.objects.create_user(username='admin', password='pass')

    def test_can_list_contacts(self):
        '''
        View all contacts without logged in
        '''
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContactDetailViewTests(APITestCase):
    '''
    Test individual Contact
    '''
    def setUp(self):
        '''
        Environement setup
        '''
        admin = User.objects.create_user(username='admin', password='pass')
        Contact.objects.create(owner=admin, depart_id=1)

    def test_can_retrieve_contact_using_valid_id(self):
        '''
        Fetch Contact with valid id
        '''
        response = self.client.get('/contacts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_contact_using_invalid_id(self):
        '''
        Fetch contact with invalid id
        '''
        response = self.client.get('/contacts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_update_contact(self):
        '''
        Edit contact
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.put('/contacts/1/', {'depart_id': 2})
        contact = Contact.objects.filter(pk=1).first()
        self.assertEqual(contact.depart_id, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_admin_contacts(self):
        '''
        Edit admin contacts
        '''
        self.client.login(username='user', password='pass')
        response = self.client.put('/contacts/1/', {'depart_id': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_update_contact(self):
        '''
        Edit admin contacts with logged out
        '''
        response = self.client.put('/contacts/1/', {'depart_id': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_contact(self):
        '''
        Delete own contact
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/contacts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_user_contact(self):
        '''
        Not allow to delete other user's contact
        '''
        admin2 = User.objects.create_user(username='admin2', password='pass')
        Contact.objects.create(owner=admin2, depart_id=2)
        self.client.login(username='admin', password='pass')
        response = self.client.delete('/contacts/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cant_delete_contact(self):
        '''
        Not allow to delete contact without logged in
        '''
        response = self.client.delete('/contacts/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
