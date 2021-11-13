from django.conf.urls import url
from knn_model.views import *

urlpatterns=[
    url('api/knnResult$', knn_result),
    url('api/user$', crud_user),
    url('api/user/(?P<pk>[0-9]+)$', crud_user_detail),
    url('api/history$', crud_history),
    url('api/history/(?P<pk>[0-9]+)$', crud_history_detail),
    url('api/message$', crud_history),
    url('api/message/(?P<pk>[0-9]+)$', crud_history_detail),
]