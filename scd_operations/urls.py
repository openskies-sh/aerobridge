
from django.urls import path
from . import views as scd_auth_views

urlpatterns = [
    path('operator_auth_test/', scd_auth_views.SCDAuthTest.as_view()),
    
]