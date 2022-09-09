'''
Views for Albums app
'''
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Album
from .serializers import AlbumSerializer


class AlbumList(APIView):
    '''
    View for list of all profiles
    '''
    serializer_class = AlbumSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        '''
        Retrieve all profiles and serialize
        '''
        albums = Album.objects.all()
        serializer = AlbumSerializer(
            albums,
            many=True,
            context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        '''
        Create an album
        '''
        serializer = AlbumSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class AlbumDetail(APIView):
    '''
    Detail view on an album
    '''
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        '''
        Fetch album by id
        '''
        try:
            album = Album.objects.get(pk=pk)
            self.check_object_permissions(self.request, album)
            return album
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Serialize album
        '''
        album = self.get_object(pk)
        serializer = AlbumSerializer(
            album,
            context={'request': request}
            )
        return Response(serializer.data)

    def put(self, request, pk):
        '''
        Edit album
        '''
        album = self.get_object(pk)
        serializer = AlbumSerializer(
            album,
            data=request.data,
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        '''
        Delete album
        '''
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
