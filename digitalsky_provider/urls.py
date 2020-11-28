from django.urls import path, re_path
from . import views as ds_views


urlpatterns = [
    path("register_drone/<uuid:pk>/", ds_views.RegisterDrone.as_view(), name="register_drone"),    
]