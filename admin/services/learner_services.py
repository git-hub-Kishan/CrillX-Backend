from django.contrib.auth import get_user_model
from django.db.models import Q
from users.helpers.model_helpers import UserType

User = get_user_model()


def get_admin_learners_queryset(
    search=None,
    status=None,
    is_active=None,
    is_verified=None,
):
    """
    Service function to fetch learners for admin table with name search and status filters.
    """
    queryset = User.objects.filter(user_type=UserType.LEARNER).select_related('learner_profile')

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
