import django.apps
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view()
def user_list(request):
    return Response("ok")


@api_view()
def user_detail(request, pk):
    return Response("user " + str(pk))
