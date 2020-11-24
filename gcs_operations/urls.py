from django.urls import path, re_path
from . import views as gcs_views


urlpatterns = [
    path('drones/', gcs_views.drone_list, name='drone-list'),
    path('drones/<uuid:drone_id>/', gcs_views.drone_detail, name='drone-detail'),
    
]