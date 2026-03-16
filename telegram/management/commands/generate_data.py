import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from telegram.models import Group, ChannelType, Channel, Description, Subscriber


class Command(BaseCommand):
    help = "Генерация тестовых данных для основных таблиц"

    def handle(self, *args, **options):
        fake = Faker(["ru_RU"])
        User = get_user_model()

        self.stdout.write("Начинаю генерацию данных...")

        # 1. Пользователь для привязки каналов
        user, _ = User.objects.get_or_create(
            username="test_generator",
            defaults={"email": "test@example.com"}
        )
        if not user.has_usable_password():
            user.set_password("test12345")
            user.save()

        # 2. Типы каналов
        public_type, _ = ChannelType.objects.get_or_create(name="публичный")
        private_type, _ = ChannelType.objects.get_or_create(name="приватный")
        channel_types = [public_type, private_type]

        # 3. Группы
        groups = []
        current_groups_count = Group.objects.count()
        groups_to_create = max(0, 1000 - current_groups_count)

        for i in range(groups_to_create):
            group = Group.objects.create(
                name=f"Группа {i + 1} - {fake.word().capitalize()}"
            )
            groups.append(group)

        if not groups:
            groups = list(Group.objects.all())
        else:
            groups = list(Group.objects.all())

        self.stdout.write(f"Групп всего: {Group.objects.count()}")

        # 4. Каналы
        channels = []
        current_channels_count = Channel.objects.count()
        channels_to_create = max(0, 1000 - current_channels_count)

        for i in range(channels_to_create):
            channel = Channel.objects.create(
                name=f"Канал {i + 1} - {fake.word().capitalize()}",
                description=fake.text(max_nb_chars=200),
                group=random.choice(groups),
                channel_type=random.choice(channel_types),
                subscribers_count=random.randint(10, 50000),
                user=user,
            )
            channels.append(channel)

        if not channels:
            channels = list(Channel.objects.all())
        else:
            channels = list(Channel.objects.all())

        self.stdout.write(f"Каналов всего: {Channel.objects.count()}")

        # 5. Описания
        current_descriptions_count = Description.objects.count()
        descriptions_to_create = max(0, 1000 - current_descriptions_count)

        for i in range(descriptions_to_create):
            channel = random.choice(channels)
            Description.objects.create(
                description=fake.text(max_nb_chars=300),
                channel=channel
            )

        self.stdout.write(f"Описаний всего: {Description.objects.count()}")

        # 6. Подписчики
        current_subscribers_count = Subscriber.objects.count()
        subscribers_to_create = max(0, 1000 - current_subscribers_count)

        for i in range(subscribers_to_create):
            channel = random.choice(channels)
            Subscriber.objects.create(
                name=fake.name(),
                telegram=channel
            )

        self.stdout.write(f"Подписчиков всего: {Subscriber.objects.count()}")

        self.stdout.write(self.style.SUCCESS("Генерация данных завершена успешно."))