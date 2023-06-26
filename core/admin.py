from django.contrib import admin
from core.models import CustomUser, Rating


class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ["passwords"]


# class RatingAdmin(admin.ModelAdmin):
#     list_display = ["rated_user", "rater", "rate", "date_added"]


# Register your models here.
# admin.site.register(Student)
admin.site.register(CustomUser)
# admin.site.register(External)
# admin.site.register(Acs)
admin.site.register(Rating)
