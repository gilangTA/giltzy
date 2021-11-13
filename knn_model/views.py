from collections import defaultdict
from django.shortcuts import render
from rest_framework.utils import json
#from django.http import HttpResponse
#from numpy.lib.function_base import append
from knn_model.models import *
import joblib
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from knn_model.serializers import *
import numpy as np

def home(request):
    return render(request, "home.html")

pfmc = joblib.load('knnPerformance.sav')
alys = joblib.load('knnAnalysis.sav')

def knn_result(request):     
        lis = []
        lis.append(12) #angka diganti request GET
        lis.append(34)
        lis.append(53)
        lis.append(31)
        lis.append(1)

        result1 = np.array(pfmc.predict([lis]))
        result1 = result1.tolist()

        result2 = np.array(alys.predict([lis]))
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