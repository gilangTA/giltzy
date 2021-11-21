from django.shortcuts import redirect, render
from knn_model.models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from knn_model.serializers import *
from django.contrib import messages
from operator import itemgetter

import joblib
import numpy as np
import pandas as pd

dataset = pd.read_csv('dataset.csv')

pfmc = joblib.load('knnPerformance.sav')
alys = joblib.load('knnAnalysis.sav')

train_data = pd.DataFrame(dataset,columns=['Hero Damage', 'Damage Taken', 'Teamfight Participation', 'Turret Damage', 'Role Id'])

@api_view(['POST','GET'])
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

            result = [{'Performance' : result1},{'Analysis' :result2}]

            return JsonResponse(result, safe=False)

#CRUD USER
@api_view(['GET', 'POST'])
def crud_user(request):
    if request.method == 'GET':
        user_get = User.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            user_get = user_get.filter(title__icontains=title)
        
        users_serializer = UserSerializer(user_get, many=True)
        return JsonResponse(users_serializer.data, safe=False)
 
    elif request.method == 'POST':
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CRUD USER Detail
@api_view(['GET', 'PUT'])
def crud_user_detail(request, pk):
    try: 
        user_get = User.objects.get(pk=pk) 
    except User.DoesNotExist: 
        return JsonResponse({'message': 'The Id does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        user_serializer = UserSerializer(user_get) 
        return JsonResponse(user_serializer.data) 

    elif request.method == 'PUT': 
        users_serializer = UserSerializer(user_get, data=request.data) 
        if users_serializer.is_valid(): 
            users_serializer.save() 
            return JsonResponse(users_serializer.data) 
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CRUD History
@api_view(['GET', 'POST', 'DELETE'])
def crud_history(request):
    if request.method == 'GET':
        history_get = History.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            history_get = history_get.filter(title__icontains=title)
        
        history_serializer = HitorySerializer(history_get, many=True)
        return JsonResponse(history_serializer.data, safe=False)
 
    elif request.method == 'POST':
        history_serializer = HitorySerializer(data=request.data)
        if history_serializer.is_valid():
            history_serializer.save()
            return JsonResponse(history_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = History.objects.all().delete()
        return JsonResponse({'message': ' History were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


#CRUD History Detail
@api_view(['GET'])
def crud_history_detail(request,pk):
    try: 
        history_get = History.objects.get(pk=pk) 
    except History.DoesNotExist: 
        return JsonResponse({'message': 'The History does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        history_serializer = HitorySerializer(history_get) 
        return JsonResponse(history_serializer.data) 

#CRUD Message
@api_view(['GET', 'POST'])
def crud_message(request):
    if request.method == 'GET':
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
@api_view(['GET'])
def crud_message_detail(request,pk):
    try: 
        message_get = Message.objects.get(pk=pk) 
    except Message.DoesNotExist: 
        return JsonResponse({'message': 'The Message does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        message_serializer = HitorySerializer(message_get) 
        return JsonResponse(message_serializer.data)

#Login
def login_view(request):    
    data_username =  User.objects.values_list('username')
    data_password =  User.objects.values_list('password')

    username_list=[]
    password_list=[]

    for i in  data_username:
        username_list.append(i)
    
    for j in  data_password:
        password_list.append(j) 

    res = list(map(itemgetter(0),username_list))
    res2 = list(map(itemgetter(0),password_list))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        i = 1
        k = len(res)
        while i < k :
            if res[i]==username and res2[i]==password:
                return knn_result(request)
                break
            i+=1
        else:
            messages.info(request, "Check username or password")
    return render(request, 'login.html')
        # if userLogin.username == '' or userLogin.password == '':
        #     messages.info(request, 'Empty Use rname or Password')
        #     #return
        # elif  userLogin.username == False or userLogin.password == False:
        #     messages.info(request, 'Wrong Username or Password')
        #     #return render('login_view')
        # else:
   

#Register
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)