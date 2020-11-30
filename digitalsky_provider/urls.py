from django.urls import path, re_path
from . import views as ds_views


urlpatterns = [
    path("register_drone/<uuid:pk>/", ds_views.RegisterDrone.as_view(), name="register_drone"),    
    path("all_permissions/", ds_views.FlyDronePermissionApplicationList.as_view(), name="download_artefact"),    
    path("apply_permission/<uuid:pk>/", ds_views.FlyDronePermissionApplicationDetail.as_view(), name="apply_permission")  
    path("download_permission_artefact/<uuid:pk>/", ds_views.DownloadFlyDronePermissionArtefact.as_view(), name="download_artefact"),  ,    
    
]