from django.urls import path
from rest_framework.routers import SimpleRouter

from study.apps import StudyConfig
from study.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView

app_name = StudyConfig.name

router = SimpleRouter()
router.register('', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/update', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('course/subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
]

urlpatterns += router.urls
