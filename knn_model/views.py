from knn_model.models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from knn_model.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

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

            result = {'performance' : result1[0]}, {'Analysis' :result2[0]}

            return JsonResponse({'performance' : result1[0]}, safe=False)

#CRUD USER
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def crud_user(request):
    User_user = request.user
    if request.method == 'PUT':
        user_detail = User.objects.get(id = User_user.id)
        user_detail.set_password(request.data['password'])
        user_detail.save()
        return JsonResponse({"Message" : "Update Successful" },safe=False ,status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        count = User_user.delete()
        return JsonResponse({'message': ' User were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

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
        
        history = History()
        history.id_user = User_history
        history.hero_name = request.data['hero_name']
        history.hero_damage = request.data['hero_damage']
        history.damage_taken = request.data['damage_taken']
        history.war_participation = request.data['war_participation']
        history.turret_damage = request.data['turret_damage']
        history.result = request.data['result']
        history.save()
        
        return JsonResponse({"Message" : "Upload History Successful" },safe=False ,status=status.HTTP_201_CREATED) 
    
    elif request.method == 'DELETE':
        count = User_history.history_set.all().delete()
        return JsonResponse({'message': ' History were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

#CRUD History Detail
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def crud_history_detail(request,pk):
#     User = request.user
#     try: 
#         history_get = User.history_set.get(pk=pk) 
#     except History.DoesNotExist: 
#         return JsonResponse({'message': 'The History does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
#     if request.method == 'GET': 
#         history_serializer = HistorySerializer(history_get) 
#         return JsonResponse(history_serializer.data) 

#CRUD Message
@api_view(['GET', 'POST', 'DELETE'])
#@permission_classes([IsAuthenticated])
def crud_message(request):
    User_message = request.user
    if request.method == 'GET':
        message_get = Message.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            message_get = message_get.filter(title__icontains=title)
        
        message_serializer = MessageSerializer(message_get, many=True)
        return JsonResponse(message_serializer.data, safe=False)
 
    elif request.method == 'POST':

        message = Message()
        message.id_user = User_message
        message.message = request.data['message']
        message.save()
        
        return JsonResponse({"message" : "Message Successful" },safe=False ,status=status.HTTP_201_CREATED) 
    
    elif request.method == 'DELETE':
        count = User_message.message_set.all().delete()
        return JsonResponse({'message': ' Message were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

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

#Register
@api_view(['POST'])
def register_user(request):
    userName = request.data['username']
    userPass = request.data['password']
    userMail = request.data['email']

    if userName and userPass and userMail:
       created = User.objects.create_user(userName, userMail, userPass)
       if created:
            return JsonResponse({'message': 'Register Success'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'there is empty field'}, status=status.HTTP_404_NOT_FOUND)