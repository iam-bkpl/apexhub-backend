from django.contrib import admin
from core.models import CustomUser, Rating


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username"]


# class RatingAdmin(admin.ModelAdmin):
#     list_display = ["rated_user", "rater", "rate", "date_added"]


# Register your models here.
# admin.site.register(Student)
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(External)
# admin.site.register(Acs)
admin.site.register(Rating)
