from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url 
from knn_model.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('user/', crud_user, name="user"),
    # path('history/', crud_history, name="history"),
    # path('message/', crud_message, name="message"),

    url('', include('knn_model.urls')),
]