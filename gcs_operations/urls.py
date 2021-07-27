from django.urls import path, re_path
from . import views as gcs_views


urlpatterns = [
    path('firmware', gcs_views.FirmwareList.as_view(), name='firmware-list'),
    path('firmware/<uuid:pk>', gcs_views.FirmwareDetail.as_view(), name='firmware-detail'),
    
    path('flight-plans', gcs_views.FlightPlanList.as_view(), name='flight-plan-list'),
    path('flight-plans/<uuid:pk>', gcs_views.FlightPlanDetail.as_view(), name='flight-plan-detail'),
    
    path('flight-operations', gcs_views.FlightOperationList.as_view(), name='flight-operation-list'),
    path('flight-operations/<uuid:pk>', gcs_views.FlightOperationDetail.as_view(), name='flight-operation-detail'),
    
    path('flight-logs', gcs_views.FlightLogList.as_view(), name='log-list'),
    path('flight-logs/<uuid:pk>', gcs_views.FlightLogDetail.as_view(), name='log-detail'),

    path("all_permissions", gcs_views.FlyDronePermissionApplicationList.as_view(), name="apply_permission"),
    path("all_permissions/<uuid:pk>", gcs_views.FlyDronePermissionApplicationDetail.as_view(), name="permission_detail"),  
    path("all_permissions/<uuid:pk>/apply", gcs_views.FlyDronePermissionApplicationSubmit.as_view(), name="permission_digitalsky_submit"),  
    
    path("files", gcs_views.CloudFileList.as_view(), name="file_list"),
    path("files/<uuid:pk>", gcs_views.CloudFileDetail.as_view(), name="file_detail"),  
    path("files/<str:document_type>/upload", gcs_views.CloudFileUpload.as_view(), name="file_upload"),  
    
]