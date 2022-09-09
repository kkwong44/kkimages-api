'''
Serializer for Comments app
'''
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    '''
    Comment serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

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
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'album', 'created_at', 'updated_at', 'content',
        ]


class CommentDetailSerializer(CommentSerializer):
    '''
    Detail serializer
    '''
    album = serializers.ReadOnlyField(source='album.id')
