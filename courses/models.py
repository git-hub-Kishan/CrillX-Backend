import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from users.helpers.model_helpers import UserType
from courses.helpers.language_helpers import CourseLanguage

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
    price = models.IntegerField(
        default=29,
        validators=[MinValueValidator(29), MaxValueValidator(9999)],
        help_text="Course price in INR (minimum ₹29, maximum ₹9999)"
    )
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

    def clean(self):
        super().clean()
        if self.price is not None and (self.price < 29 or self.price > 9999):
            raise ValidationError({'price': 'Course price must be between ₹29 and ₹9999.'})
        if not self.is_published and self.is_locked:
            raise ValidationError({'is_locked': 'An unpublished (draft) course cannot be locked.'})

    def __str__(self):
        return f"{self.course_name} by {self.user.email}"


class CourseModule(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course = models.ForeignKey(
        CreatorCourse,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    module_title = models.CharField(max_length=255)
    what_you_will_learn = models.TextField(
        blank=True, 
        null=True, 
        help_text="Key takeaways and learning objectives for this module"
    )
    module_thumbnail = models.CharField(max_length=500, blank=True, null=True)
    module_video = models.CharField(max_length=500, blank=True, null=True)
    duration_in_seconds = models.PositiveIntegerField(
        default=0, 
        help_text="Duration of the video in seconds"
    )
    order = models.PositiveIntegerField(
        default=1, 
        help_text="Order/position of the module in the course"
    )
    is_preview = models.BooleanField(
        default=False, 
        help_text="Whether this module is available as a free preview"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.order}. {self.module_title} ({self.course.course_name})"

