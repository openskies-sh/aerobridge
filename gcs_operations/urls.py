from django.urls import path, re_path
from . import views as gcs_views


urlpatterns = [
    path('transaction', gcs_views.TransactionList.as_view(), name='transaction-list'),
    path('transaction/<uuid:transaction_id>', gcs_views.TransactionDetail.as_view(), name='transaction-detail'),
    
]