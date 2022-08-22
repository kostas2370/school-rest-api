from django.contrib import admin
from django.urls import path,re_path,include

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("api.urls")),
    path('api/auth/',include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view())
]
