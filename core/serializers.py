from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from core.models import Acs, External, Student


class StudentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Student
    fields = ['id','user','first_name','last_name','gender','address','program','enrollment_date']
    fields = '__all__'
  
 
class ExternalSerializer(serializers.ModelSerializer):
  class Meta:
   model = External
   fields = ['id','user','name','address','phone_number','website','description','created_at']
   
  
class AcsSerializer(serializers.ModelSerializer):
 class Meta:
  model = Acs
  fields = ['id','user','website']