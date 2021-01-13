from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from pki_framework.utils import requires_scopes, BearerAuth
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
import json

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class PingView(View):        
    def get(self, request):
        return HttpResponse(json.dumps({"message":"pong"}))


class HomeView(TemplateView):
    template_name = 'jetway/home.html'
