from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from core.models import Acs, CustomUser, External, Student

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):     
  # user = CustomUserSerializer(read_only=True)
  user = serializers.CharField(read_only=True,max_length=4)
  class Meta:
    model = Student
    fields = ['id','user','first_name','last_name','gender','address','program','enrollment_date']
  
 
class ExternalSerializer(serializers.ModelSerializer):
  class Meta:
   model = External
   fields = ['id','user','name','address','phone_number','website','description','created_at']
   
  
class AcsSerializer(serializers.ModelSerializer):
 class Meta:
  model = Acs
  fields = ['id','user','website']
  
  
class UserSerializer(BaseUserSerializer):
  class Meta(BaseUserSerializer.Meta):
    fields = "__all__"
    