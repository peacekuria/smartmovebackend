from celery_app import celery_app

@celery_app.task
def periodic_cleanup_task():
    """
    Celery task for periodic cleanup operations (e.g., deleting old data, clearing caches).
    """
    print("Running periodic cleanup task...")
    # Placeholder for actual cleanup logic
    # Example: delete_old_guest_data()
    # Example: clear_expired_tokens()
    print("Periodic cleanup task completed.")
    return "Cleanup task executed."
