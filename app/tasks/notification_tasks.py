from celery_app import celery_app
from app.services.notification_service import NotificationService

@celery_app.task
def send_notification_task(user_id, message, notification_type):
    """
    Celery task to send a user notification asynchronously.
    """
    print(f"Attempting to send {notification_type} notification to user {user_id}: {message}")
    NotificationService.send_notification(user_id, message, notification_type)
    print(f"Notification task completed for user {user_id}.")
    return f"Notification to user {user_id} scheduled."
