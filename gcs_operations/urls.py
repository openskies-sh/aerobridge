from django.urls import path, re_path
from . import views as gcs_views


urlpatterns = [
    path('transaction', gcs_views.TransactionList.as_view(), name='transaction-list'),
    path('transaction/<uuid:transaction_id>', gcs_views.TransactionDetail.as_view(), name='transaction-detail'),
    path('flight-plans', gcs_views.FlightPlanList.as_view(), name='transaction-list'),
    path('flight-plans/<uuid:flightplan_id>', gcs_views.FlightPlanDetail.as_view(), name='transaction-detail'),
    path('flight-operations', gcs_views.FlightOperationList.as_view(), name='transaction-list'),
    path('flight-operations/<uuid:flightoperation_id>', gcs_views.FlightOperationDetail.as_view(), name='transaction-detail'),
    
    
]