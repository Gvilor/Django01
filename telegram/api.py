from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from telegram.models import Channel, Group, Description, ChannelType, Subscriber
from telegram.serializers import ChannelSerializer, GroupSerializer, DescriptionSerializer, ChannelTypeSerializer, SubscriberSerializer

class ChannelViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class GroupViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ChannelTypeViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = ChannelType.objects.all()
    serializer_class = ChannelTypeSerializer

class DescriptionViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

class SubscriberViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer