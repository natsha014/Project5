from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(source='study', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson_count', 'lessons')

    @staticmethod
    def get_lesson_count(instance):
        return instance.study.count()
