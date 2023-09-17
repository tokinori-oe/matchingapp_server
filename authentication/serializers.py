from django.contrib.auth.models import User, Group
from rest_framework import serializers

#HyperlinkedModelSerializerは、リレーションフィールド（ForeignKeyやManyToManyFieldなど）をハイパーリンクとして表現するために使用される
#HyperlinkedModelSerializerを使用すると、モデル間のリレーションシップをハイパーリンクとして表現できるため、特定のフィールドに対してCharField()や他のフィールドタイプを使わずにシリアライズできる
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: #モデルとシリアライザの設定を定義するためのメタクラスmodelとかfieldsの情報が最低限必要
        model = User #HyperlinkedModelSerializerは明示的にモデルを指定する必要がある
        fields = ['username','email','password'] #シリアライザがモデルからシリアライズするフィールドを指定する
        extra_kwargs = {'password':{'write_only':True}} #パスワードをシリアライズしないように設定する
        
    def create(self, validated_data):#createメソッドのオーバーライド
        user=User.objects.create_user(**validated_data)
        '''
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password( password=validated_data['password'])
        user.save()
        '''
        return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField() # ログイン時に送信されるユーザー名（ユーザー名やメールアドレスなど）を処理するためのフィールドを定義
    #CharFieldは文字列を表すフィールドで、バリデーションや変換が行われる、尚このフィールドはjson形式のデータについてのフィールドである
    password = serializers.CharField(write_only=True) 