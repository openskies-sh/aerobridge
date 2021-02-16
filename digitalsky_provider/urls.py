from django.urls import path, re_path
from . import views as ds_views

urlpatterns = [
    path("aircraft_roster/", ds_views.AircraftRegisterList.as_view(), name="sign_drone_list"),    
    path("aircraft_roster/<uuid:pk>", ds_views.AircraftRegisterDetail.as_view(), name="sign_drone"),    
    path("register_aircraft/<uuid:pk>", ds_views.RegisterDrone.as_view(), name="register_drone"),    
    
    path("all_permissions", ds_views.FlyDronePermissionApplicationList.as_view(), name="permission_list"),    
    path("apply_permission/<uuid:pk>", ds_views.FlyDronePermissionApplicationDetail.as_view(), name="apply_permission"),
    path("all_permissions/<uuid:pk>", ds_views.DownloadFlyDronePermissionArtefact.as_view(), name="download_artefact"),  
    
    # path("uin_applications/", ds_views.UINApplicationList.as_view(), name="list_uins"),    
    # path("uin_applications/<uuid:pk>", ds_views.UINApplicationDetail.as_view(), name="uin_detail") , 
    # path("submit_uin_application/<uuid:uin_application_id>", ds_views.SubmitUINApplication.as_view(), name="submit_uin_application"), 
    
    path("submit_log/<uuid:operation_id>", ds_views.SubmitSignedFlightLog.as_view(), name="submit_flight_log"),
    
    path('logs/', ds_views.LogList.as_view(), name='digitalsky-log-list'),
    path('logs/<uuid:log_id>', ds_views.LogDetail.as_view(), name='digitalsky-log-detail'),
      
]