'''
Views for Albums app
'''
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
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
