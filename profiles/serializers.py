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
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        '''
        Get is_owner method
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''
        Set profile fields
        '''
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image', 'is_owner'
        ]
