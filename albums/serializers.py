from rest_framework import serializers
from .models import Album


class AlbumSerializer(serializers.ModelSerializer):
    '''
    Album serialize with read only
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_cover_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px'
            )
        return value

    def get_is_owner(self, obj):
        '''
        Get is_owner method
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''
        Set album fields
        '''
        model = Album
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'category', 'title', 'content',
            'cover_image', 'category_filter',
        ]
