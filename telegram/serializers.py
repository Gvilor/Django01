from rest_framework import serializers

from telegram.models import Group, Channel, Description, ChannelType, Subscriber

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class ChannelSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        allow_null=True,
        required=False
    )
    class Meta:
        model = Channel
        fields = ['id', 'name', 'group', 'channel_type']

class ChannelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelType
        fields = "__all__"

class DescriptionSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    
    class Meta:
        model = Description
        fields = "__all__"

class SubscriberSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True,)  
    
    class Meta:
        model = Subscriber
        fields = "__all__"

