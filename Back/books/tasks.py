from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# will not send email if user has no email
@shared_task
def send_order_confirmation_email(borrow_id, user_email):
    subject = "Borrowing Confirmation"
    message = f"Your borrowing request with ID {borrow_id} has been received and is being processed."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])