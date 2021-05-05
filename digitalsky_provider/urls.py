from django.urls import path, re_path
from . import views as ds_views

urlpatterns = [
    path("all_permissions", ds_views.FlyDronePermissionApplicationList.as_view(), name="permission_list"),    
    path("apply_permission/<uuid:pk>", ds_views.FlyDronePermissionApplicationDetail.as_view(), name="apply_permission"),
    path("all_permissions/<uuid:pk>", ds_views.DownloadFlyDronePermissionArtefact.as_view(), name="download_artefact"),  
    
    path('logs/', ds_views.LogList.as_view(), name='digitalsky-log-list'),
    path('logs/<uuid:log_id>', ds_views.LogDetail.as_view(), name='digitalsky-log-detail'),
      
]