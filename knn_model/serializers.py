from knn_model.models import *
from rest_framework import serializers
from django.forms import ModelForm

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id_user', 'email', 'username', 'password']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        #fields = ['hero_name','hero_damage','turret_damage','damage_taken','war_participation','result']
        fields = '__all__'

    # def to_representation(self, instance):
    #         self.fields['id_user'] =  User.objects.get('id')
    #         return super(HitorySerializer, self).to_representation(instance)  

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'