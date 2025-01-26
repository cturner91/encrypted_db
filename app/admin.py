from django.contrib import admin

from .models import AppUser, Message


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'encrypted__user_from', 'encrypted__user_to', 'encrypted__content']


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Message, MessageAdmin)
