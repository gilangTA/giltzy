import json
import re
from django.shortcuts import redirect, render
from numpy.core.records import array
from knn_model.models import *
from django.http import JsonResponse, response
from rest_framework.decorators import api_view
from rest_framework import status
from knn_model.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User

import joblib
import numpy as np
import pandas as pd

dataset = pd.read_csv('dataset.csv')

pfmc = joblib.load('knnPerformance.sav')
alys = joblib.load('knnAnalysis.sav')

train_data = pd.DataFrame(dataset,columns=['Hero Damage', 'Damage Taken', 'Teamfight Participation', 'Turret Damage', 'Role Id'])

@api_view(['POST','GET'])
#@permission_classes([IsAuthenticated])
def knn_result(request):
    #User = request.user
    if request.method == 'POST':
            test_data = pd.DataFrame({"Hero Damage" : request.POST['hero_damage'],
                                      "Damage Taken" : request.POST['damage_taken'],
                                      "Teamfight Participation" : request.POST['war_participation'],
                                      "Turret Damage" : request.POST['turret_damage'],
                                      "Role Id" : request.POST['role_id']
                                    }, index=[0])

            test_data = train_data.append(test_data, ignore_index=True)

            newMax = 1
            newMin = 0
            
            test_data['Hero Damage'] = (test_data['Hero Damage'].astype(float) - test_data['Hero Damage'].astype(float).min()) * (newMax - newMin)  / (test_data['Hero Damage'].astype(float).max() - test_data['Hero Damage'].astype(float).min()) + newMin
            test_data["Damage Taken"] = (test_data["Damage Taken"].astype(float) - test_data["Damage Taken"].astype(float).min()) * (newMax - newMin)  / (test_data["Damage Taken"].astype(float).max() - test_data["Damage Taken"].astype(float).min()) + newMin
            test_data["Teamfight Participation"] = (test_data["Teamfight Participation"].astype(float) - test_data["Teamfight Participation"].astype(float).min()) * (newMax - newMin)  / (test_data["Teamfight Participation"].astype(float).max() - test_data["Teamfight Participation"].astype(float).min()) + newMin
            test_data["Turret Damage"] = (test_data["Turret Damage"].astype(float) - test_data["Turret Damage"].astype(float).min()) * (newMax - newMin)  / (test_data["Turret Damage"].astype(float).max() - test_data["Turret Damage"].astype(float).min()) + newMin

            test_data = test_data.tail(1)
            
            result1 = pfmc.predict(test_data)
            result2 = alys.predict(test_data)

            result1 = result1.tolist()
            result2 = result2.tolist()

            result = [{'Performance' : result1},{'Analysis' :result2}]

            return JsonResponse(result, safe=False)

# #CRUD USER
# @api_view(['GET', 'POST'])
# def crud_user(request):
#     if request.method == 'GET':
#         user_get = User.objects.all()
        
#         title = request.query_params.get('title', None)
#         if title is not None:
#             user_get = user_get.filter(title__icontains=title)
        
#         users_serializer = UserSerializer(user_get, many=True)
#         return JsonResponse(users_serializer.data, safe=False)
 
#     elif request.method == 'POST':
#         users_serializer = UserSerializer(data=request.data)
#         if users_serializer.is_valid():
#             users_serializer.save()
#             return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #CRUD USER Detail
# @api_view(['GET', 'PUT'])
# def crud_user_detail(request, pk):
    # try: 
    #     user_get = User.objects.get(pk=pk) 
    # except User.DoesNotExist: 
    #     return JsonResponse({'message': 'The Id does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # if request.method == 'GET': 
    #     user_serializer = UserSerializer(user_get) 
    #     return JsonResponse(user_serializer.data) 

    # elif request.method == 'PUT': 
    #     users_serializer = UserSerializer(user_get, data=request.data) 
    #     if users_serializer.is_valid(): 
    #         users_serializer.save() 
    #         return JsonResponse(users_serializer.data) 
    #     return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CRUD History
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def crud_history(request):
    User_history = request.user
    if request.method == 'GET':
        history_get = User_history.history_set.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            history_get = history_get.filter(title__icontains=title)
        
        history_serializer = HistorySerializer(history_get, many=True)
        return JsonResponse(history_serializer.data, safe=False)
 
    elif request.method == 'POST':
        # history_serializer = HistorySerializer(data = request.data)
        
        history = History()
        history.id_user = User_history
        history.hero_name = request.data['hero_name']
        history.hero_damage = request.data['hero_damage']
        history.damage_taken = request.data['damage_taken']
        history.war_participation = request.data['war_participation']
        history.turret_damage = request.data['turret_damage']
        history.result = request.data['result']
        history.save()
        # if history_serializer.is_valid():            
        #     history_serializer.save()
        
        return JsonResponse({"Message" : "Upload History Successful" },safe=False ,status=status.HTTP_201_CREATED) 
        # return JsonResponse(history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = History.objects.all().delete()
        return JsonResponse({'message': ' History were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

#CRUD History Detail
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crud_history_detail(request,pk):
    User = request.user
    try: 
        history_get = User.history_set.get(pk=pk) 
    except History.DoesNotExist: 
        return JsonResponse({'message': 'The History does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        history_serializer = HistorySerializer(history_get) 
        return JsonResponse(history_serializer.data) 

#CRUD Message
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def crud_message(request):
    #User = request.user
    if request.method == 'GET':
        #message_get = User.message_set.all()
        message_get = Message.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            message_get = message_get.filter(title__icontains=title)
        
        message_serializer = MessageSerializer(message_get, many=True)
        return JsonResponse(message_serializer.data, safe=False)
 
    elif request.method == 'POST':
        message_serializer = MessageSerializer(data=request.data)
        if message_serializer.is_valid():
            message_serializer.save()
            return JsonResponse(message_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CRUD Message Detail
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def crud_message_detail(request,pk):
    # User = request.user
    # try: 
    #     message_get = User.message_set.get(pk=pk) 
    # except Message.DoesNotExist: 
    #     return JsonResponse({'message': 'The Message does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    # if request.method == 'GET': 
    #     message_serializer = MessageSerializer(message_get) 
    #     return JsonResponse(message_serializer.data)

#Token LOGIN
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['usernane'] = user.username
        token['email'] = user.email
        token['password'] = user.password
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer