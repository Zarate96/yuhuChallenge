import threading
from django.core.mail import send_mail
from django.conf import settings
def send_task_notification(email, task_title, action):
    """Function to send email notifications asynchronously using threading"""
    subject = f"Tarea {action}: {task_title}"
    message = f"Tu tarea '{task_title}' ha sido {action} correctamente."
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def send_email_async(email, task_title, action):
    """Runs the email sending function in a separate thread"""
    thread = threading.Thread(target=send_task_notification, args=(email, task_title, action))
    print(f"Sending email to {email} for task {task_title}.")
    thread.start()
