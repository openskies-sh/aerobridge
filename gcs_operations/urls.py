from django.urls import path, re_path
from . import views as gcs_views


urlpatterns = [
    # path('transaction', gcs_views.TransactionList.as_view(), name='transaction-list'),
    # path('transaction/<uuid:transaction_id>', gcs_views.TransactionDetail.as_view(), name='transaction-detail'),
    
    path('firmware', gcs_views.FirmwareList.as_view(), name='firmware-list'),
    path('firmware/<uuid:firmware_id>', gcs_views.FirmwareDetail.as_view(), name='firmware-detail'),
    
    path('flight-plans', gcs_views.FlightPlanList.as_view(), name='flight-plan-list'),
    path('flight-plans/<uuid:flightplan_id>', gcs_views.FlightPlanDetail.as_view(), name='flight-plan-detail'),
    
    path('flight-operations', gcs_views.FlightOperationList.as_view(), name='flight-operation-list'),
    path('flight-operations/<uuid:flightoperation_id>', gcs_views.FlightOperationDetail.as_view(), name='flight-operation-detail'),
    
    path('flight-logs', gcs_views.FlightLogList.as_view(), name='log-list'),
    path('flight-logs/<uuid:flightlog_id>', gcs_views.FlightLogDetail.as_view(), name='log-detail'),
    
]