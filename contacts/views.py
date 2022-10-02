'''
Views for contacts app
'''
from rest_framework import generics, permissions
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Contact
from .serializers import ContactSerializer


class ContactList(generics.ListCreateAPIView):
    '''
    Generic views to list contacts
    plus conditional filterset field
    '''
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Contact.objects.all()

    def perform_create(self, serializer):
        '''
        and to create contact
        '''
        serializer.save()


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Generic views to edit and delete contact
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
