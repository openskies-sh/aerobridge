# Create your views here.
from rest_framework import generics, mixins
from .models import Incident
from .serializers import IncidentSerializer
from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
# Create your views here.

