'''
Project serializers
'''
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    '''
    Set current user serializer
    '''
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    staff = serializers.ReadOnlyField(source='profile.staff')

    class Meta(UserDetailsSerializer.Meta):
        '''
        Add fields to serializer
        '''
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image', 'staff')
