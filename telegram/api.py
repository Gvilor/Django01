from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView


from telegram.models import Channel, Group, Description, ChannelType, Subscriber
from telegram.serializers import ChannelSerializer, GroupSerializer, DescriptionSerializer, ChannelTypeSerializer, SubscriberSerializer

class ChannelViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_superuser:
            user_id = self.request.GET.get("user")
            if user_id:
                qs = qs.filter(user_id=user_id)
            return qs

        return qs.filter(user=self.request.user)

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

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "is_superuser": request.user.is_superuser,
        })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "ok"})