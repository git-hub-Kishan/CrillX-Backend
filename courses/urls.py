from django.urls import path
from courses.views.course_views import (
    CreatorCourseAPIView,
    CreatorCourseDetailAPIView,
    CourseModuleListCreateAPIView,
)

urlpatterns = [
    path('', CreatorCourseAPIView.as_view(), name='creator-course-list-create'),
    path('<uuid:course_uuid>/', CreatorCourseDetailAPIView.as_view(), name='creator-course-detail'),
    path('<uuid:course_uuid>/modules/', CourseModuleListCreateAPIView.as_view(), name='creator-course-module-list-create'),

    # test urls
    path('<uuid:course_uuid>', CreatorCourseDetailAPIView.as_view(), name='creator-course-detail-no-slash'),
    path('<uuid:course_uuid>/modules', CourseModuleListCreateAPIView.as_view(), name='creator-course-module-list-create-no-slash'),
]

