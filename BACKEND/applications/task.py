from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import Flask
from applications.model import *
from applications.database import db
from applications.workers import celery_init_app
from celery import shared_task


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False



mail = Mail(app)
celery = celery_init_app(app)

@shared_task()
def check_and_send_reminders():
    with app.app_context():
        threshold_date = datetime.now() 
        # Query for borrowed books with return dates within the threshold or past due
        borrowed_books = BorrowedBooks.query.filter(BorrowedBooks.due_date <= threshold_date).all()
        
        for book in borrowed_books:
            user = User.query.get(book.user_id)
            if user:
                # Customize the message and subject as needed
                subject = "Library Book Return Reminder"
                message = f"Dear {user.name},\n\nThis is a reminder to return the book '{book.title}' by {book.due_date.strftime('%Y-%m-%d')}. Please visit the library to return the book.\n\nThank you!"
                
                # Send the notification email
                send_book_notification.delay(user.email, subject, message)

        return f"Checked {len(borrowed_books)} borrowed books for reminders."


@celery.task()
def send_book_notification(email, subject, message):
    with app.app_context():
        msg = Message(
            subject,
            sender="test@example.com",
            recipients=[email]
        )
        msg.body = message
        mail.send(msg)
        return f"Email sent to {email}"

@shared_task()
def send_reminder_notifications(message):
    with app.app_context():
        msg = Message(
            subject="Hello from 8.30",
            sender="test@example.com",
            recipients=["user@gmail.com"]
        )
        msg.body = message
        mail.send(msg)
        return message

@shared_task(ignore_result=False)
def hello_world():
    import time
    for i in range(1, 6):
        print(i)
        time.sleep(1)

    print("Hello Celery") 
