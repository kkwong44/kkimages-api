'''
Views for Albums app
'''
from rest_framework import generics, permissions
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Album
from .serializers import AlbumSerializer


class AlbumList(generics.ListCreateAPIView):
    '''
    Generic views to list albums
    '''
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Album.objects.all()

    def perform_create(self, serializer):
        '''
        and to create album
        '''
        serializer.save(owner=self.request.user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Generic views to edit and delete profile
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
