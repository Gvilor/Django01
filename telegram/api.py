from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from telegram.models import Telegram
from telegram.serializers import TelegramSerializer

class TelegramViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Telegram.objects.all()
    serializer_class = TelegramSerializer