'''
Serializer for Contacts app
'''
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    '''
    Contact serialize with read only
    '''

    class Meta:
        '''
        Set contact fields
        '''
        model = Contact
        fields = [
            'id', 'depart_id', 'department', 'created_at', 'updated_at',
            'contact', 'address', 'town', 'county', 'postcode', 'telephone',
            'email',
        ]
