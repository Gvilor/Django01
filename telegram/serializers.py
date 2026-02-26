from rest_framework import serializers

from telegram.models import Group,Telegram

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class TelegramSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Telegram
        fields = ['id', 'name', 'group', 'description']

