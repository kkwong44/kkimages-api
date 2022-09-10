'''
Serializer for Likes app
'''
from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    '''
    Like serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_is_owner(self, obj):
        '''
        Get is_owner method
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''
        Set comment fields
        '''
        model = Like
        fields = [
            'id', 'owner', 'album', 'created_at'
        ]

    def create(self, validated_data):
        '''
        Check duplicate likes
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
