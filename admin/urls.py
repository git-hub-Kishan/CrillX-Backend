from django.urls import path
from admin.views.auth_views import AdminLoginAPIView
from admin.views.creator_views import AdminCreatorListAPIView
from admin.views.learner_views import AdminLearnerListAPIView
from admin.views.user_views import AdminUserKPIAPIView, AdminUserStatusUpdateAPIView

app_name = 'admin_api'

urlpatterns = [
    path('login/', AdminLoginAPIView.as_view(), name='admin-login'),
    path('users/stats/', AdminUserKPIAPIView.as_view(), name='admin-user-stats'),
    path('users/status/', AdminUserStatusUpdateAPIView.as_view(), name='admin-user-status'),
    path('users/creators/', AdminCreatorListAPIView.as_view(), name='admin-creator-list'),
    path('users/learners/', AdminLearnerListAPIView.as_view(), name='admin-learner-list'),
]
