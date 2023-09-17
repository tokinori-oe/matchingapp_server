from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from profiling.models import UserProfile
from profiling.serializers import UserProfileSerializer

# Create your views here.

#トークンを受け取ってidを返すビュー,get()関数を用いる
class IDfromTokenView(APIView):
    authentication_classes = [TokenAuthentication] #ここでトークン情報を受け取り認証する
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        return Response({'user_id': user_id}, status=status.HTTP_200_OK)
        
class AccountInfoFromIDView(APIView):
    def get(self, request):
        try:
            account_id = request.query_params.get('user_id')
        
            # アカウントモデルから指定されたidのアカウントを取得
            account = UserProfile.objects.get(user_id=account_id)
            serializer = UserProfileSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ChangeProfileInfoView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            account_id = request.query_params.get('user_id')
            user_profile = UserProfile.objects.get(user_id=account_id)
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
