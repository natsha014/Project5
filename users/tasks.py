from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def block_inactive_users():
    """Блокирует пользователей, которые не заходили более 30 дней."""
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lte=month_ago,
        is_active=True,
        is_superuser=False
    )

    if inactive_users.exists():
        inactive_users.update(is_active=False)
