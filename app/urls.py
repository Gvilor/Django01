from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from telegram import views
from telegram.api import (
    ChannelViewset,
    GroupViewset,
    ChannelTypeViewset,
    DescriptionViewset,
    SubscriberViewset
)

router = DefaultRouter()
router.register("channels", ChannelViewset, basename="channel")
router.register("groups", GroupViewset, basename="group")
router.register("channel-types", ChannelTypeViewset, basename="channeltype")
router.register("descriptions", DescriptionViewset, basename="description")
router.register("subscribers", SubscriberViewset, basename="subscriber")

urlpatterns = [
    path('', views.ShowTelegramView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)