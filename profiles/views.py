'''
Profiles Views
'''
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from kkimages_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    '''
    View for list of all profiles
    '''
    def get(self, request):
        '''
        Retrieve all profiles and serialize
        '''
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles,
            many=True,
            context={'request': request}
            )
        return Response(serializer.data)


class ProfileDetail(APIView):
    '''
    Detail view on a profile
    '''
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        '''
        Fetch profile by id
        '''
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Serialize profile
        '''
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile,
            context={'request': request}
            )
        return Response(serializer.data)

    def put(self, request, pk):
        '''
        Edit profile
        '''
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
