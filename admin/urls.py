from django.urls import path
from admin.views.auth_views import AdminLoginAPIView
from admin.views.creator_views import (
    AdminCreatorListAPIView,
    AdminCreatorDetailAPIView,
    AdminCreatorCoursesAPIView,
    AdminCreatorCourseModulesAPIView,
)
from admin.views.learner_views import AdminLearnerListAPIView
from admin.views.user_views import AdminUserKPIAPIView, AdminUserStatusUpdateAPIView
from admin.views.header_gif_views import (
    AdminHeaderGIFListCreateAPIView,
    AdminHeaderGIFDetailAPIView,
)

app_name = 'admin_api'

urlpatterns = [
    path('login/', AdminLoginAPIView.as_view(), name='admin-login'),

    path('users/stats/', AdminUserKPIAPIView.as_view(), name='admin-user-stats'),
    path('users/status/', AdminUserStatusUpdateAPIView.as_view(), name='admin-user-status'),

    path('users/creators/', AdminCreatorListAPIView.as_view(), name='admin-creator-list'),
    path('users/creators/<str:creator_identifier>/', AdminCreatorDetailAPIView.as_view(), name='admin-creator-detail'),
    path('users/creators/<str:creator_identifier>/courses/', AdminCreatorCoursesAPIView.as_view(), name='admin-creator-courses'),
    path('users/creators/<str:creator_identifier>/courses/<str:course_identifier>/modules/', AdminCreatorCourseModulesAPIView.as_view(), name='admin-creator-course-modules'),
    
    path('users/learners/', AdminLearnerListAPIView.as_view(), name='admin-learner-list'),

    # Header GIF Manager Endpoints
    path('header-gifs/', AdminHeaderGIFListCreateAPIView.as_view(), name='admin-header-gif-list-create'),
    path('header-gifs/<str:identifier>/', AdminHeaderGIFDetailAPIView.as_view(), name='admin-header-gif-detail'),
]
