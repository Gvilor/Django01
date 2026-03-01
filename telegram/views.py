from django.http import HttpResponse
from django.views import View
from typing import Any
from telegram.models import Channel
from django.views.generic import TemplateView

class ShowTelegramView(TemplateView):
    template_name = "telegrams/show_telegrams.html"

    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['telegram'] = Channel.objects.all()

        return context