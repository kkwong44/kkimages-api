'''
Serializer for profiles
'''
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Profile serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        '''
        Set profile fields
        '''
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image'
        ]
