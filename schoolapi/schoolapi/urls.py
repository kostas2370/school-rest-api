from django.contrib import admin
from django.urls import path,re_path,include
from api.registerview import RegisterApi
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("api.urls")),
    path('api/auth/',include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('api/register/',RegisterApi.as_view()),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
