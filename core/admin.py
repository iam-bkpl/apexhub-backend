from django.contrib import admin
from core.models import Acs, CustomUser, External, Student

# Register your models here.
admin.site.register(Student)
admin.site.register(CustomUser)
admin.site.register(External)
admin.site.register(Acs)