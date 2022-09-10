'''
Serializer for Followers app
'''
from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    '''
    Follower serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    def get_is_owner(self, obj):
        '''
        Get is_owner method
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''
        Set follower fields
        '''
        model = Follower
        fields = [
            'id', 'owner', 'followed_name', 'followed', 'created_at'
        ]

    def create(self, validated_data):
        '''
        Check duplicate follows
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
