import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.helpers.location_helpers import State
from users.helpers.model_helpers import (
    ExperienceRange,
    Profession,
    SignupType,
    TeachingCategory,
    UserType,
)
from users.helpers.language_helpers import CourseLanguage


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    signup_type = models.CharField(
        max_length=20,
        choices=SignupType.choices,
        default=SignupType.EMAIL
    )
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.LEARNER
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    yt_username = models.CharField(max_length=100, blank=True, null=True)
    insta_username = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    state = models.CharField(
        max_length=10,
        choices=State.choices
    )
    city = models.CharField(max_length=100)
    teaching_category = models.CharField(
        max_length=50,
        choices=TeachingCategory.choices,
        blank=True,
        null=True
    )
    experience = models.CharField(
        max_length=20,
        choices=ExperienceRange.choices,
        blank=True,
        null=True
    )
    profession = models.CharField(
        max_length=50,
        choices=Profession.choices,
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CreatorProfile: {self.user.email}"


class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner_profile')
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    state = models.CharField(
        max_length=10,
        choices=State.choices
    )
    city = models.CharField(max_length=100)
    profession = models.CharField(
        max_length=50,
        choices=Profession.choices,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LearnerProfile: {self.user.email}"



