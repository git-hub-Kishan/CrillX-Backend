import uuid
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from users.helpers.model_helpers import UserType
from courses.models import CreatorCourse, CourseModule

User = get_user_model()


def get_admin_creators_queryset(
    search=None,
    status=None,
    is_active=None,
    is_verified=None,
):
    """
    Service function to fetch creators for admin table with name search and status filters.
    """
    queryset = User.objects.filter(user_type=UserType.CREATOR).select_related('creator_profile')

    # 1. Search ONLY by name
    if search:
        search = search.strip()
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    # 2. Status filter
    if status:
        st = status.strip().lower()
        if st == 'active':
            queryset = queryset.filter(is_active=True)
        elif st == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif st == 'verified':
            queryset = queryset.filter(is_verified=True)
        elif st == 'unverified':
            queryset = queryset.filter(is_verified=False)

    # 3. Explicit Boolean filters
    if is_active is not None:
        if str(is_active).strip().lower() in ('true', '1'):
            queryset = queryset.filter(is_active=True)
        elif str(is_active).strip().lower() in ('false', '0'):
            queryset = queryset.filter(is_active=False)

    if is_verified is not None:
        if str(is_verified).strip().lower() in ('true', '1'):
            queryset = queryset.filter(is_verified=True)
        elif str(is_verified).strip().lower() in ('false', '0'):
            queryset = queryset.filter(is_verified=False)

    return queryset.order_by('-created_at')


def get_admin_creator_by_identifier(identifier):
    """
    Lookup a creator user by UUID, integer ID, email, or username.
    Returns User instance if found and is a creator, else None.
    """
    if not identifier:
        return None

    identifier_str = str(identifier).strip()

    # 1. Try UUID lookup
    try:
        val = uuid.UUID(identifier_str)
        creator = User.objects.filter(uuid=val, user_type=UserType.CREATOR).select_related('creator_profile').first()
        if creator:
            return creator
    except (ValueError, AttributeError):
        pass

    # 2. Try integer ID lookup
    if identifier_str.isdigit():
        creator = User.objects.filter(id=int(identifier_str), user_type=UserType.CREATOR).select_related('creator_profile').first()
        if creator:
            return creator

    # 3. Try email or username lookup
    creator = User.objects.filter(
        Q(email__iexact=identifier_str) | Q(username__iexact=identifier_str),
        user_type=UserType.CREATOR
    ).select_related('creator_profile').first()

    return creator


def get_admin_creator_courses_queryset(
    creator,
    search=None,
    language=None,
    status_param=None,
    min_price=None,
    max_price=None,
):
    """
    Fetch all courses created by a specific creator with modules count, search and filtering.
    """
    queryset = CreatorCourse.objects.filter(user=creator).annotate(
        modules_count=Count('modules')
    )

    # Search by course name
    if search:
        queryset = queryset.filter(course_name__icontains=search.strip())

    # Language filter
    if language:
        queryset = queryset.filter(course_language=language.strip().lower())

    # Status filter: published / draft / locked
    if status_param:
        st = status_param.strip().lower()
        if st == 'draft':
            queryset = queryset.filter(is_published=False)
        elif st == 'locked':
            queryset = queryset.filter(is_published=True, is_locked=True)
        elif st == 'published':
            queryset = queryset.filter(is_published=True, is_locked=False)

    # Price range filters
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


def get_admin_course_by_identifier(course_identifier, creator=None):
    """
    Lookup a CreatorCourse by UUID or integer ID, optionally scoped to a specific creator.
    """
    if not course_identifier:
        return None

    course_identifier_str = str(course_identifier).strip()
    queryset = CreatorCourse.objects.select_related('user', 'user__creator_profile').prefetch_related('modules')

    if creator:
        queryset = queryset.filter(user=creator)

    # 1. Try UUID
    try:
        val = uuid.UUID(course_identifier_str)
        course = queryset.filter(uuid=val).first()
        if course:
            return course
    except (ValueError, AttributeError):
        pass

    # 2. Try integer ID
    if course_identifier_str.isdigit():
        course = queryset.filter(id=int(course_identifier_str)).first()
        if course:
            return course

    return None


def get_admin_course_modules_queryset(course, search=None):
    """
    Fetch all modules for a course ordered by module order and created_at, with optional search.
    """
    queryset = CourseModule.objects.filter(course=course)
    if search:
        search_term = search.strip()
        queryset = queryset.filter(
            Q(module_title__icontains=search_term) |
            Q(what_you_will_learn__icontains=search_term)
        )
    return queryset.order_by('order', 'created_at')
