from django.shortcuts import HttpResponse
from django.views import View


class ACSHome(View):
    def get(self, request):
        return HttpResponse("Hello world acs")
