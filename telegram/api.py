from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Count, Max, Min
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from openpyxl import Workbook
from openpyxl.styles import Font

from rest_framework import mixins, serializers, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from telegram.models import Channel, Group, Description, ChannelType, Subscriber
from telegram.serializers import (
    ChannelSerializer,
    GroupSerializer,
    DescriptionSerializer,
    ChannelTypeSerializer,
    SubscriberSerializer,
)
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

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField(allow_null=True)
        max = serializers.IntegerField(allow_null=True)
        min = serializers.IntegerField(allow_null=True)

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        queryset = self.get_queryset()

        stats = queryset.aggregate(
            count=Count("*"),
            avg=Avg("subscribers_count"),
            max=Max("subscribers_count"),
            min=Min("subscribers_count"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        queryset = self.get_queryset()

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Channels"

        headers = [
            "ID",
            "Название",
            "Описание",
            "Группа",
            "Тип канала",
            "Количество подписчиков",
        ]

        worksheet.append(headers)

        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        for channel in queryset:
            worksheet.append([
                channel.id,
                channel.name,
                channel.description,
                channel.group.name if channel.group else "",
                channel.channel_type.name if channel.channel_type else "",
                channel.subscribers_count,
            ])

        worksheet.column_dimensions["A"].width = 10
        worksheet.column_dimensions["B"].width = 30
        worksheet.column_dimensions["C"].width = 50
        worksheet.column_dimensions["D"].width = 25
        worksheet.column_dimensions["E"].width = 20
        worksheet.column_dimensions["F"].width = 25

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="channels.xlsx"'

        workbook.save(response)
        return response

class GroupViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField(allow_null=True)
        max = serializers.IntegerField(allow_null=True)
        min = serializers.IntegerField(allow_null=True)

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = Group.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class ChannelTypeViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ChannelType.objects.all()
    serializer_class = ChannelTypeSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField(allow_null=True)
        max = serializers.IntegerField(allow_null=True)
        min = serializers.IntegerField(allow_null=True)

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = ChannelType.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class DescriptionViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField(allow_null=True)
        max = serializers.IntegerField(allow_null=True)
        min = serializers.IntegerField(allow_null=True)

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = Description.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class SubscriberViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField(allow_null=True)
        max = serializers.IntegerField(allow_null=True)
        min = serializers.IntegerField(allow_null=True)

    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request):
        stats = Subscriber.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Неверный логин или пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)

        return Response({
            "id": user.id,
            "username": user.username,
            "is_superuser": user.is_superuser,
        })

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"detail": "Вы вышли"})

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "is_superuser": user.is_superuser,
        })

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=["get"])
    def csrf(self, request):
        return Response({"detail": "CSRF cookie set"})