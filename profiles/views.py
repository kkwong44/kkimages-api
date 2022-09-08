'''
Profiles Views
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    '''
    View for list of profiles
    '''
    def get(self, request):
        '''
        Retrieve all profiles and serialize
        '''
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
