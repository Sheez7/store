from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User

new_user_registered = Signal()

new_order = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
   Sends an email with the reset password token.
    When a token is created, an email needs to be sent to the user.

    Args:
    sender: View Class that sent the signal
    instance: View Instance that sent the signal
    reset_password_token: Token Model Object
    kwargs:

    Returns:
    None
    """

    # Send an e-mail to the user
    subject = f"Password Reset Token for {reset_password_token.user}"
    message = reset_password_token.key
    from_email = settings.EMAIL_HOST_USER
    to_email = [reset_password_token.user.email]
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.send()


@receiver(new_user_registered)
def send_email_confirmation(user_id, **kwargs):
    """
    Sends an email with a confirmation token to the user
    """
    # Get or create a confirmation token for the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    # Compose the email
    email_title = f"Email confirmation Token for {token.user.email}"
    email_message = token.key
    email_from = settings.EMAIL_HOST_USER
    email_to = [token.user.email]

    # Send the email
    msg = EmailMultiAlternatives(email_title, email_message, email_from, email_to)
    msg.send()


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        subject="Order status update",
        body='The order has been placed',
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    # Send the email
    msg.send()