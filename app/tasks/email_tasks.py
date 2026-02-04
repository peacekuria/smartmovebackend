from celery_app import celery_app
from app.services.email_service import EmailService

@celery_app.task
def send_email_task(recipient, subject, body):
    """
    Celery task to send an email asynchronously.
    """
    print(f"Attempting to send email to {recipient} with subject '{subject}'...")
    EmailService.send_email(recipient, subject, body)
    print(f"Email task completed for {recipient}.")
    return f"Email to {recipient} scheduled."
