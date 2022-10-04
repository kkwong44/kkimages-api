'''
Serializer for profiles
'''
from rest_framework import serializers
from followers.models import Follower
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Profile serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    albums_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        '''
        Get is_owner method
        '''
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        '''
        Check and return follower id
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        '''
        Set profile fields
        '''
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'email', 'content', 'image', 'is_owner', 'following_id',
            'albums_count', 'followers_count', 'following_count',
            'staff',
        ]
