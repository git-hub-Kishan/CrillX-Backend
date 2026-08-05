import logging
import threading
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

logger = logging.getLogger(__name__)


def _send_email_task(subject, plain_message, from_email, recipient_list, html_message):
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
    except Exception as e:
        logger.warning(f"Failed to send email to {recipient_list}: {str(e)}")


def send_otp_email(email, otp, user_name=None, user_type=None, async_send=True):
    """
    Common helper to send OTP email using HTML template in a non-blocking background thread.
    """
    try:
        subject = f"Your CrillX Verification OTP: {otp}"

        context = {
            'otp': otp,
            'user_name': user_name or email,
            'user_type': str(user_type or 'learner').lower(),
        }
        html_message = render_to_string('emails/otp_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'CrillX <noreply@crillx.com>')

        if async_send:
            thread = threading.Thread(
                target=_send_email_task,
                args=(subject, plain_message, from_email, [email], html_message)
            )
            thread.daemon = True
            thread.start()
        else:
            _send_email_task(subject, plain_message, from_email, [email], html_message)

        return True
    except Exception as e:
        logger.warning(f"Error preparing OTP email for {email}: {str(e)}")
        return False


def send_password_changed_alert(user, async_send=True):
    """
    Sends a security alert email when a user's password is changed.
    """
    try:
        subject = "Security Alert: Your CrillX Password Was Changed"

        context = {
            'user_name': user.first_name or user.email,
            'time_stamp': timezone.now().strftime('%d %B %Y at %H:%M UTC')
        }
        html_message = render_to_string('emails/password_changed.html', context)
        plain_message = strip_tags(html_message)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'CrillX <noreply@crillx.com>')

        if async_send:
            thread = threading.Thread(
                target=_send_email_task,
                args=(subject, plain_message, from_email, [user.email], html_message)
            )
            thread.daemon = True
            thread.start()
        else:
            _send_email_task(subject, plain_message, from_email, [user.email], html_message)
        
        return True
    except Exception as e:
        logger.error(f"Error preparing password changed alert email: {str(e)}")
        return False


def send_forgot_password_otp_email(email, otp, user_name=None, async_send=True):
    """
    Send forgot password OTP email using HTML template in a non-blocking background thread.
    """
    try:
        subject = f"CrillX Password Reset Code: {otp}"

        context = {
            'otp': otp,
            'user_name': user_name or email,
        }
        html_message = render_to_string('emails/forgot_password_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'CrillX <noreply@crillx.com>')

        if async_send:
            thread = threading.Thread(
                target=_send_email_task,
                args=(subject, plain_message, from_email, [email], html_message)
            )
            thread.daemon = True
            thread.start()
        else:
            _send_email_task(subject, plain_message, from_email, [email], html_message)

        return True
    except Exception as e:
        logger.warning(f"Error preparing forgot password OTP email for {email}: {str(e)}")
        return False


def send_welcome_email(user, async_send=True):
    """
    Send welcome email to user upon successful profile creation.
    Wrapped in try-except so email failure never breaks profile creation.
    """
    try:
        if not user or not getattr(user, 'email', None):
            return False

        email = user.email
        user_name = getattr(user, 'full_name', '') or getattr(user, 'first_name', '') or email
        raw_user_type = str(getattr(user, 'user_type', 'learner')).lower()

        subject = f"Welcome to CrillX, {user_name}!"

        context = {
            'user_name': user_name,
            'user_type': raw_user_type,
        }


        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'CrillX <noreply@crillx.com>')

        if async_send:
            thread = threading.Thread(
                target=_send_email_task,
                args=(subject, plain_message, from_email, [email], html_message)
            )
            thread.daemon = True
            thread.start()
        else:
            _send_email_task(subject, plain_message, from_email, [email], html_message)

        return True
    except Exception as e:
        logger.warning(f"Failed to process welcome email for {getattr(user, 'email', 'unknown')}: {str(e)}")
        return False
