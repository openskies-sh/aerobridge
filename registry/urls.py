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
from . import views as registryviews
from django.urls import path

urlpatterns = [

    path('aircraft/', registryviews.AircraftList.as_view()),        
    path('aircraft/<uuid:pk>', registryviews.AircraftDetail.as_view()),
    path('aircraft/rfm/<str:flight_controller_id>', registryviews.AircraftRFMDetail.as_view()),
    path('operators/', registryviews.OperatorList.as_view()),
    path('operators/<uuid:pk>', registryviews.OperatorDetail.as_view()),  
    path('manufacturers/', registryviews.ManufacturerList.as_view()),
    path('manufacturers/<uuid:pk>', registryviews.ManufacturerDetail.as_view()),  

]