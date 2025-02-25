from django.contrib import admin
from .models import User, UserConfirmation


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(User, UserAdmin)
admin.site.register(UserConfirmation, UserConfirmationAdmin)
