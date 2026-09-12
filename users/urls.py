from django.urls import path
from users.views.auth_views import (
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    GoogleLoginAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
    RegisterAPIView,
    ResendOTPAPIView,
    ResetPasswordAPIView,
    VerifyForgotPasswordOTPAPIView,
    VerifyOTPAPIView,
)
from users.views.profile_views import CreateProfileAPIView, MeAPIView ,ProfileAPIView
from users.views.s3_views import S3PresignedUrlAPIView
from admin.views.header_gif_views import ActiveHeaderGIFAPIView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('google-login/', GoogleLoginAPIView.as_view(), name='google-login'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend-otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('forgot-password/verify-otp/', VerifyForgotPasswordOTPAPIView.as_view(), name='forgot-password-verify-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token-refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    
    path('profile/create/', CreateProfileAPIView.as_view(), name='create-profile'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    
    path('s3/presigned-url/', S3PresignedUrlAPIView.as_view(), name='s3-presigned-url'),
    path('header-gif/active/', ActiveHeaderGIFAPIView.as_view(), name='public-header-gif-active'),
]






