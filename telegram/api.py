from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from telegram.models import Channel, Group, Description, ChannelType, Subscriber
from telegram.serializers import ChannelSerializer, GroupSerializer, DescriptionSerializer, ChannelTypeSerializer, SubscriberSerializer

class ChannelViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class GroupViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ChannelTypeViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ChannelType.objects.all()
    serializer_class = ChannelTypeSerializer

class DescriptionViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

class SubscriberViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer