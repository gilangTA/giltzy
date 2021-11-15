from django.db.models import fields
from knn_model.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'email', 'username', 'password']

class HitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id_history','hero_name', 'hero_damage', 'turret_damage', 'damage_taken', 'war_participation', 'result']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id_message', 'id_user', 'message']