from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserLoginSerializer
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import status

class CheckUsernameView(APIView):
    def post(self, request, format=None):
        # POSTリクエストのデータからユーザーネームを取得
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        username_to_check = request.data.get('username', '')
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error":', '.join(e.messages)},status=status.HTTP_400_BAD_REQUEST) #どういう意味？
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error":"Invalid mail address"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # ユーザーネームをデータベースで検索
            user = User.objects.get(username=username_to_check)
            return Response({"message": "this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User can be registered"}, status=status.HTTP_200_OK)

    
class UserLoginView(APIView): #APIViewはどういうクラス？APIビューはWeb APIエンドポイントのロジックを定義し、リクエストを処理してレスポンスを返す役割を果たす
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password) #authenticateはユーザーデータと自動で照合してくれる。照合したらユーザーオブジェクトを返す。しなかった場合はNoneを返す
            if user:
                token, created = Token.objects.get_or_create(user=user) #特定のユーザーに関連するトークンを取得し、存在しない場合はトークンを作成する
                return Response({'token':token.key})
            else:
                return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
