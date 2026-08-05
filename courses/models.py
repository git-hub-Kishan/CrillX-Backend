import uuid
from django.db import models
from django.contrib.auth import get_user_model
from users.helpers.model_helpers import UserType
from users.helpers.language_helpers import CourseLanguage

User = get_user_model()

class CreatorCourse(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='courses',
        limit_choices_to={'user_type': UserType.CREATOR}
    )
    course_name = models.CharField(max_length=255)
    description = models.TextField(help_text="Course description (100-200 words)")
    course_language = models.CharField(
        max_length=5,
        choices=CourseLanguage.choices,
        default=CourseLanguage.ENGLISH
    )
    course_thumbnail = models.CharField(max_length=500, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_name} by {self.user.email}"
