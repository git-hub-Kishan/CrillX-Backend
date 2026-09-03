from django.db.models import Q
from courses.models import CreatorCourse, CourseModule
from courses.serializers.course_serializers import CreatorCourseSerializer, CourseModuleSerializer


def create_course(user, data):
    """
    Service function to validate and create a new course for a creator.
    """
    serializer = CreatorCourseSerializer(data=data)
    if not serializer.is_valid():
        return False, serializer.errors

    course = serializer.save(user=user)
    return True, CreatorCourseSerializer(course).data


def get_user_courses_queryset(user, search=None, language=None, status_param=None, min_price=None, max_price=None):
    """
    Service function to fetch courses created by a specific user with optional search, language, status, and price range filters.
    """
    queryset = CreatorCourse.objects.filter(user=user)

    if search:
        search = search.strip()
        queryset = queryset.filter(
            Q(course_name__icontains=search) | Q(description__icontains=search)
        )

    if language:
        queryset = queryset.filter(course_language=language.strip())

    if status_param:
        st = status_param.strip().lower()
        if st in ('published', 'active'):
            queryset = queryset.filter(is_published=True, is_locked=False)
        elif st in ('draft', 'drafted', 'unpublished'):
            queryset = queryset.filter(is_published=False)
        elif st == 'locked':
            queryset = queryset.filter(is_published=True, is_locked=True)

    if min_price is not None:
        try:
            queryset = queryset.filter(price__gte=int(min_price))
        except (ValueError, TypeError):
            pass

    if max_price is not None:
        try:
            queryset = queryset.filter(price__lte=int(max_price))
        except (ValueError, TypeError):
            pass

    return queryset.order_by('-created_at')


def get_course(user, course_uuid):
    """
    Service function to fetch a single course by UUID for the owning creator.
    """
    try:
        course = CreatorCourse.objects.get(uuid=course_uuid, user=user)
        return True, CreatorCourseSerializer(course).data
    except CreatorCourse.DoesNotExist:
        return False, {"detail": "Course not found."}


def update_course(user, course_uuid, data):
    """
    Service function to partially update a course (one or many fields) by UUID.
    """
    try:
        course = CreatorCourse.objects.get(uuid=course_uuid, user=user)
    except CreatorCourse.DoesNotExist:
        return False, {"detail": "Course not found."}

    serializer = CreatorCourseSerializer(course, data=data, partial=True)
    if not serializer.is_valid():
        return False, serializer.errors

    updated_course = serializer.save()
    return True, CreatorCourseSerializer(updated_course).data


def create_course_modules(user, course_uuid, data):
    """
    Service function to create one or multiple modules for a course owned by the creator.
    Supports a single dict, a list of dicts, or a dict containing a 'modules' key.
    """
    try:
        course = CreatorCourse.objects.get(uuid=course_uuid, user=user)
    except CreatorCourse.DoesNotExist:
        return False, {"detail": "Course not found or permission denied."}

    if isinstance(data, dict) and "modules" in data and isinstance(data["modules"], list):
        modules_list = data["modules"]
    elif isinstance(data, list):
        modules_list = data
    elif isinstance(data, dict):
        modules_list = [data]
    else:
        return False, {"detail": "Invalid payload format. Expected a module object, a list of module objects, or {'modules': [...]}."}

    if not modules_list:
        return False, {"detail": "At least one module object must be provided."}

    serializer = CourseModuleSerializer(data=modules_list, many=True)
    if not serializer.is_valid():
        return False, serializer.errors

    created_modules = serializer.save(course=course)
    return True, CourseModuleSerializer(created_modules, many=True).data


def get_course_modules_queryset(user, course_uuid):
    """
    Service function to fetch modules queryset for a course owned by the creator.
    """
    try:
        course = CreatorCourse.objects.get(uuid=course_uuid, user=user)
    except CreatorCourse.DoesNotExist:
        return False, {"detail": "Course not found."}

    return True, course.modules.all()

