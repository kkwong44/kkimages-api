'''
Views for Albums app
'''
from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Album
from .serializers import AlbumSerializer


class AlbumList(generics.ListCreateAPIView):
    '''
    Generic views to list albums
    with additional annotate count fields and filter
    plus search fields and conditional filterset fields
    '''
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Album.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        photos_count=Count('photo', distinct=True),
    ).order_by('-updated_at', '-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',

    ]
    search_fields = [
        'owner__username',
        'title',
        'category_filter',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'photos_count',
        'likes__created_at',
        'comments__created_at',
        'photos__created_at',
    ]

    def perform_create(self, serializer):
        '''
        and to create album
        '''
        serializer.save(owner=self.request.user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Generic views to edit and delete profile
    with additional annotate count fields
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Album.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        photos_count=Count('photo', distinct=True),
    ).order_by('created_at')
    serializer_class = AlbumSerializer
