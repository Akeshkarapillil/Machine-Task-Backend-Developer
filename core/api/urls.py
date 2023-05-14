from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', get_routes),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', LoginAPI.as_view()),
    path('user/', UserAPI.as_view()),
    path('overview/', OverviewAPI.as_view()),
    path('create/', CreateAPI.as_view()),
    path('detail/<int:id>', DetailAPI.as_view()),
    path('update/<int:id>', UpdateAPI.as_view()),
    path('delete/<int:id>', DeleteAPI.as_view()),
    path('tag/', TagListAPI.as_view()),
    path('tag/detail/', TagDetailAPI.as_view()),
]