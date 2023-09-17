from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User

# Create your views here.
class SchoolNameView(APIView):
    
    def get(self, request, *args, **kwargs):
        school_options =['東京大学','京都大学','大阪大学','東北大学','九州大学','名古屋大学','北海道大学','東京工業大学','一橋大学']
        response_data={'schoolOptions':school_options}
        
        return Response(response_data, status=status.HTTP_200_OK)
    

class AccountRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_data = response.data
        user = User.objects.get(username=user_data['username'])
        user_id = user.id
        user_data['user_id'] = user_id
        
        return Response(user_data, status.HTTP_201_CREATED)
        
    
class ProfileRegistrationView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    
    