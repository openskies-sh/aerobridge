"""ohio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views as registryviews
from django.urls import path, re_path
from django.conf import settings


urlpatterns = [
    
    path('operators', registryviews.OperatorList.as_view()),
    path('operators/<uuid:pk>', registryviews.OperatorDetail.as_view()),    
    
    path('aircrafts', registryviews.AircraftList.as_view()),        
    path('aircrafts/<uuid:pk>', registryviews.AircraftDetail.as_view()),
    
    path('pilots', registryviews.PilotList.as_view()),
    path('pilots/<uuid:pk>', registryviews.PilotDetail.as_view()),
    
]
