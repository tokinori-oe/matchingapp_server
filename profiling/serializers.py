# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class ProfileSerializerForRecommendation(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['school_name', 'faculty', 'department', 'hobbies', 'profile', 'age', 'grade']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
    def create(self, validated_data):
        profile = UserProfile(**validated_data)
        profile.save()
        return profile
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # パスワードを書き込み専用フィールドとして追加

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  

    def create(self, validated_data):
        # パスワードをハッシュ化してUserオブジェクトを作成
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user