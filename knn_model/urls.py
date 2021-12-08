from django.conf.urls import url
from django.urls import path
from knn_model.views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns=[
    path('knnResult/', knn_result),

    path('user/', crud_user),
    
    path('history/', crud_history),
    
    path('message/', crud_message),

    path('registerUser/', register_user),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
