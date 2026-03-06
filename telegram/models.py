from django.db import models


class Group(models.Model):
    name = models.TextField("Группа")
    picture = models.ImageField(
        "Картинка",
        upload_to="groups/",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class ChannelType(models.Model):
    name = models.CharField("Тип канала", max_length=50)
    picture = models.ImageField(
        "Картинка",
        upload_to="channel_types/",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Тип канала"
        verbose_name_plural = "Типы каналов"

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Группа"
    )
    channel_type = models.ForeignKey(
        ChannelType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Тип канала"
    )
    subscribers_count = models.PositiveIntegerField("Количество подписчиков", default=0)
    picture = models.ImageField(
        "Картинка",
        upload_to="channels/",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name


class Description(models.Model):
    description = models.TextField("Описание")
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        null=True,
        related_name='descriptions',
        verbose_name="Канал"
    )

    class Meta:
        verbose_name = "Описание"
        verbose_name_plural = "Описания"

    def __str__(self):
        return self.description[:30]


class Subscriber(models.Model):
    name = models.CharField("Имя", max_length=100)
    telegram = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name="Канал"
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return self.name