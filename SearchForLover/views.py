from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Q
from profiling.models import UserProfile
from profiling.serializers import UserProfileSerializer, ProfileSerializerForRecommendation
from .serializers import RequestSerializer
from .models import RequestForLoverModel

# Create your views here.
class GetRecommendation(APIView):
    def get(self, request):
        try:
            account_id = request.query_params.get('user_id')
            user_profile = UserProfile.objects.get(user_id=account_id)
            user_hobbies = user_profile.hobbies
            user_gender = user_profile.gender
            filter_condition = Q(hobbies=user_hobbies) & ~Q(gender=user_gender)
            filtered_profiles = UserProfile.objects.filter(filter_condition) #ここfilter使うとサーバー負荷が重すぎる
            serializer = UserProfileSerializer(filtered_profiles, many=True)
            #print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

class GetRequestView(generics.CreateAPIView):
    serializer_class = RequestSerializer
    