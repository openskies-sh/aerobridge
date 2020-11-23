"""aerobridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from gcs_operations import views as gcs_views
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drones/', gcs_views.DroneList.as_view(), name='drone-list'),
    path('drones/<uuid:pk>/', gcs_views.DroneDetail.as_view(), name='drone-detail'),
    path('drones/<uuid:pk>/create', gcs_views.DroneCreate.as_view(), name='drone-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)