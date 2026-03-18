from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from study.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправляет сообщение пользователю об обновлении курса, но не раньше, чем через 4 часа после обновления"""
    course = Course.objects.get(pk=course_id)
    now = timezone.now()

    if course.last_update_email_sent:
        delta = now - course.last_update_email_sent
        if delta < timedelta(hours=4):
            print(f"Рассылка для курса {course.name} уже была {delta} назад. Пропускаем.")
            return

    subscriptions = Subscription.objects.filter(course=course)

    recipient_list = [sub.user.email for sub in subscriptions]

    if recipient_list:
        send_mail(
            subject=f'Обновление курса: {course.name}',
            message=f'Материалы курса "{course.name}" были обновлены. Заходите проверить!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )

        course.last_update_email_sent = now
        course.save()
