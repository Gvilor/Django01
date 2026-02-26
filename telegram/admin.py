from django.contrib import admin

from telegram.models import Telegram, Group
# Register your models here.
@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'description', 'group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','name']