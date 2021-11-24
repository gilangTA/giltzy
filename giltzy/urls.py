from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url 
from knn_model.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('knn_model.urls')),
    url('api/history/(?P<pk>[0-9]+)$', crud_history_detail),
    #url('api/message/(?P<pk>[0-9]+)$', crud_message_detail),
]