from django.contrib import admin
from telegram.models import Group, Channel, Description, ChannelType, Subscriber

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description' ,'group', 'channel_type', 'subscribes']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'channel']

@admin.register(ChannelType)
class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'telegram']