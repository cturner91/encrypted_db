from django.contrib import admin

from .models import AppUser, Message


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_from', 'user_to', 'content']


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Message, MessageAdmin)
