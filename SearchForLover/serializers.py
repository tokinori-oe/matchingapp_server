from rest_framework import serializers
from .models import RequestForLoverModel

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForLoverModel
        fields = '__all__'
    def create(self, validated_data):
        request_info = RequestForLoverModel(**validated_data)
        request_info.save()
        return request_info