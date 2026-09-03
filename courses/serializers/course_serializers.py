from rest_framework import serializers
from courses.models import CreatorCourse
from courses.helpers.language_helpers import CourseLanguage
from utils.s3_utils import get_file_url


class CreatorCourseSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = CreatorCourse
        fields = [
            'uuid',
            'course_name',
            'description',
            'price',
            'course_language',
            'course_thumbnail',
            'is_published',
            'is_locked',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid', 'status', 'created_at', 'updated_at']

    def get_status(self, obj):
        if not obj.is_published:
            return 'draft'
        if obj.is_locked:
            return 'locked'
        return 'published'

    def validate_course_name(self, value):
        if value and len(value) > 80:
            raise serializers.ValidationError("Course title cannot exceed 80 characters.")
        return value

    def validate_price(self, value):
        if value is not None and (value < 29 or value > 9999):
            raise serializers.ValidationError("Course price must be between ₹29 and ₹9999.")
        return value

    def validate_course_language(self, value):
        if value and value not in CourseLanguage.values:
            raise serializers.ValidationError(
                f"Invalid course language '{value}'. Choose from: {CourseLanguage.values}"
            )
        return value

    def validate(self, attrs):
        # Determine effective values for is_published and is_locked
        is_published = attrs.get('is_published', self.instance.is_published if self.instance else True)
        is_locked = attrs.get('is_locked', self.instance.is_locked if self.instance else False)

        if not is_published and is_locked:
            raise serializers.ValidationError({
                "is_locked": "An unpublished (draft) course cannot be locked. Publish the course before locking it."
            })

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('course_thumbnail'):
            data['course_thumbnail'] = get_file_url(data['course_thumbnail'])
        return data


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        from courses.models import CourseModule
        model = CourseModule
        fields = [
            'uuid',
            'module_title',
            'what_you_will_learn',
            'module_thumbnail',
            'module_video',
            'duration_in_seconds',
            'order',
            'is_preview',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']

    def validate_module_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Module title is required.")
        return value.strip()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('module_thumbnail'):
            data['module_thumbnail'] = get_file_url(data['module_thumbnail'])
        if data.get('module_video'):
            data['module_video'] = get_file_url(data['module_video'])
        return data

