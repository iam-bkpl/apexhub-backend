from django.contrib import admin
from core.models import Acs, CustomUser, External, Student

class CustomUserAdmin(admin.ModelAdmin):
  readonly_fields = ['passwords']

# Register your models here.
admin.site.register(Student)
admin.site.register(CustomUser)
admin.site.register(External)
admin.site.register(Acs)