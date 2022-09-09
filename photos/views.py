'''
Views for photos app
'''
from rest_framework import generics, permissions
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Photo
from .serializers import PhotoSerializer, PhotoDetailSerializer


class PhotoList(generics.ListCreateAPIView):
    '''
    Generic views to list photos
    '''
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        '''
        and to create photo
        '''
        serializer.save(owner=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Generic views to edit and delete photos
    '''
    permissions_classes = [IsOwnerOrReadOnly]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()
