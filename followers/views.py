'''
Views for followers app
'''
from rest_framework import generics, permissions
from kkimages_api.permissions import IsOwnerOrReadOnly
from followers.models import Follower
from followers.serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    '''
    Generic views to list followers
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        '''
        and to create follower
        '''
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    '''
    Generic views to delete follower
    '''
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
