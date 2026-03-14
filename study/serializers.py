from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson
from study.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='study', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson_count', 'is_subscribed', 'lessons')

    @staticmethod
    def get_lesson_count(instance):
        return instance.study.count()

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return instance.subscriptions.filter(user=user).exists()
