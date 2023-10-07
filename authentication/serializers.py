from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: #モデルとシリアライザの設定を定義するためのメタクラスmodelとかfieldsの情報が最低限必要
        model = User #HyperlinkedModelSerializerは明示的にモデルを指定する必要がある
        fields = ['username','email','password'] 
        extra_kwargs = {'password':{'write_only':True}} #パスワードをシリアライズしないように設定する
        
    def create(self, validated_data):#createメソッドのオーバーライド
        user=User.objects.create_user(**validated_data)
        return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField() # ログイン時に送信されるユーザー名（ユーザー名やメールアドレスなど）を処理するためのフィールドを定義
    password = serializers.CharField(write_only=True) 