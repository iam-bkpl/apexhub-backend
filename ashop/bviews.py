from django.shortcuts import HttpResponse
from django.views import View


class Home(View):
  def get(self, request):
    return HttpResponse("Hello ashop")