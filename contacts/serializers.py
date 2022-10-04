'''
Serializer for Contacts app
'''
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    '''
    Contact serialize with read only
    '''
    staff = serializers.ReadOnlyField(source='owner.is_staff')

    class Meta:
        '''
        Set contact fields
        '''
        model = Contact
        fields = [
            'id', 'owner', 'depart_id', 'department', 'created_at',
            'updated_at', 'contact', 'address', 'town', 'county',
            'postcode', 'telephone', 'email', 'staff',
        ]
