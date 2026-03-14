from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from study.models import Course, Lesson, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class StudyTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.user.set_password("12345")
        self.user.save()

        self.moderator = User.objects.create(email="mod@test.ru", is_staff=True)
        from django.contrib.auth.models import Group
        mod_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(mod_group)

        self.course = Course.objects.create(name="Django", description="Test", owner=self.user)
        self.lesson = Lesson.objects.create(name="Intro", course=self.course, owner=self.user)

    def test_lesson_retrieve(self):
        """Тест просмотра урока владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("study:lesson_retrieve", args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тест создания урока"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "New Lesson", "course": self.course.pk, "description": "New"}
        response = self.client.post(reverse("study:lesson_create"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_delete_by_moderator(self):
        """Тест: модератор НЕ может удалять уроки"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse("study:lesson_delete", args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("study:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Updated Name"}
        url = reverse("study:lesson_update", args=[self.lesson.pk])

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Updated Name")

    def test_subscription_toggle(self):
        """Тест работы подписки (добавление/удаление)"""
        self.client.force_authenticate(user=self.user)
        data = {"course": self.course.pk}
        url = reverse("study:subscribe")

        # Подписываемся
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписываемся
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
