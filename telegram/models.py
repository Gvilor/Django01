from django.db import models

class Group(models.Model):
    name = models.TextField("Група")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группа"

    def __str__(self):
        return self.name

class Telegram(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    