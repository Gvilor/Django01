from rest_framework import serializers
from telegram.models import Group, Channel, Description, ChannelType, Subscriber

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class ChannelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if "request" in self.context:
            validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    class Meta:
        model = Channel
        fields = "__all__"

class ChannelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelType
        fields = "__all__"

class DescriptionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Description
        fields = "__all__"

class SubscriberSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subscriber
        fields = "__all__"

