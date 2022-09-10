'''
Views for profiles app
'''
from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    '''
    Generic views to list all profiles
    with additional annotate count fields and filter
    plus search fields and conditional filterset fields
    '''
    queryset = Profile.objects.annotate(
        albums_count=Count('owner__album', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'albums_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Generic views to edit and delete profile
    with additional annotate count fields
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        albums_count=Count('owner__album', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('created_at')
    serializer_class = ProfileSerializer
