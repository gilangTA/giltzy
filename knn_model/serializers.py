from django.db.models import fields
from knn_model.models import *
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id_user', 'email', 'username', 'password']

class HitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'