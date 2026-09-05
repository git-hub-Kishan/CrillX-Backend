from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from users.helpers.model_helpers import UserType

User = get_user_model()


def get_user_kpis():
    """
    Fetch high-level user KPI metrics in a single aggregated SQL query.
    Calculates metrics across creators and learners.
    """
    stats = User.objects.filter(
        user_type__in=[UserType.CREATOR, UserType.LEARNER]
    ).aggregate(
        total_users=Count('id'),
        total_creators=Count('id', filter=Q(user_type=UserType.CREATOR)),
        total_learners=Count('id', filter=Q(user_type=UserType.LEARNER)),
        active_users=Count('id', filter=Q(is_active=True)),
    )

    return {
        "total_users": stats.get('total_users') or 0,
        "total_creators": stats.get('total_creators') or 0,
        "total_learners": stats.get('total_learners') or 0,
        "active_users": stats.get('active_users') or 0,
    }


def toggle_user_status(user_identifiers, current_admin_user, is_active_override=None):
    """
    Toggle or update is_active status for one or multiple users by UUIDs or IDs.
    If is_active_override is None, flips the current status (is_active = not is_active).
    Prevents an admin from deactivating their own account.
    """
    if not isinstance(user_identifiers, (list, tuple, set)):
        user_identifiers = [user_identifiers]

    clean_ids = [str(x).strip() for x in user_identifiers if x is not None and str(x).strip()]
    if not clean_ids:
        return False, "No user ID or UUID provided."

    # Fetch users matching either uuid or id
    users = list(
        User.objects.filter(
            Q(uuid__in=clean_ids) | Q(id__in=[int(i) for i in clean_ids if i.isdigit()])
        ).exclude(id=current_admin_user.id)
    )

    if not users:
        return False, "No valid users found or cannot modify your own account."

    updated_users = []
    for u in users:
        if is_active_override is not None:
            u.is_active = bool(is_active_override)
        else:
            u.is_active = not u.is_active
        u.save(update_fields=['is_active', 'updated_at'])

        updated_users.append({
            "uuid": str(u.uuid),
            "name": u.full_name or u.username,
            "is_active": u.is_active
        })

    return True, updated_users
