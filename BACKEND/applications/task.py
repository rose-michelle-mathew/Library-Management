from collections import defaultdict
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import Flask, render_template
from sqlalchemy import func
from applications.mailing import format_message, send_email
from applications.model import *
from applications.database import db
from applications.workers import celery_init_app
from celery import shared_task


app = Flask(__name__,template_folder='BACKEND/templates')
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
        threshold_date = datetime.now() + timedelta(days=2)
        borrowed_books = BorrowedBooks.query.filter(BorrowedBooks.due_date <= threshold_date).all()
        
        # Group borrowed books by user
        user_books = defaultdict(list)
        for borrowed_book in borrowed_books:
            user_books[borrowed_book.user_id].append(borrowed_book)

        # Send email for each user
        for user_id, books in user_books.items():
            user = User.query.get(user_id)
            if user:
                book_list = ""
                for book in books:
                    book_details = Book.query.get(book.book_id)
                    if book_details:
                        book_list += f"'{book_details.name}' due by {book.due_date.strftime('%Y-%m-%d')}\n"
                
                # Customize the message and subject as needed
                subject = "Library Book Return Reminder"
                message = (
                    f"Dear {user.username},\n\n"
                    f"This is a reminder to return the following books:\n\n"
                    f"{book_list}\n"
                    f"Please visit the library to return the books.\n\n"
                    f"Thank you!"
                )
                
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
def generate_monthly_report_data():
    today = datetime.today()
    first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)

    # Query issued books
    issued_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.issue_date >= first_day_of_last_month,
        BorrowedBooks.issue_date <= last_day_of_last_month
    ).all()

    # Query returned books
    returned_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.due_date >= first_day_of_last_month,
        BorrowedBooks.due_date <= last_day_of_last_month
    ).all()

    # Query overdue books
    overdue_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.due_date < today,
        BorrowedBooks.due_date == None
    ).all()

    # Prepare data for template
    issued_books = [{'borrowed': borrowed, 'book': book, 'user': user} for borrowed, book, user in issued_books_data]
    returned_books = [{'borrowed': borrowed, 'book': book, 'user': user} for borrowed, book, user in returned_books_data]
    overdue_books = [{'borrowed': borrowed, 'book': book, 'user': user} for borrowed, book, user in overdue_books_data]

    return {
        'first_day_of_last_month': first_day_of_last_month,
        'last_day_of_last_month': last_day_of_last_month,
        'issued_books': issued_books,
        'returned_books': returned_books,
        'overdue_books': overdue_books,
    }

@shared_task(ignore_result=False)

def send_monthly_activity_report():
    today = datetime.today()
    first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)

    # Query issued books
    issued_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.issue_date >= first_day_of_last_month,
        BorrowedBooks.issue_date <= last_day_of_last_month
    ).all()

    # Query overdue books
    overdue_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.due_date < today
    ).all()

    # Query number of books borrowed by section
    books_by_section = db.session.query(
        Section.section_name, func.count(AllActivity.id)
    ).select_from(AllActivity).join(Book, AllActivity.book_id == Book.id).join(Section, Book.section_id == Section.id).filter(
        AllActivity.status == 'borrowed',
        AllActivity.requested_date >= first_day_of_last_month,
        AllActivity.requested_date <= last_day_of_last_month
    ).group_by(Section.section_name).all()
    # # Debugging: Print the data to ensure correctness
    # print("Issued Books Data:", issued_books_data)
    # print("Overdue Books Data:", overdue_books_data)
    # print("Books by Section Data:", books_by_section) # Prepare the data for the report


    data = {
        'issued_books': [
            {
                'book_name': book.Book.name,
                'user': book.User.username,
                'issue_date': book.BorrowedBooks.issue_date.strftime('%Y-%m-%d'),
                'due_date': book.BorrowedBooks.due_date.strftime('%Y-%m-%d')
            }
            for book in issued_books_data
        ],
        'overdue_books': [
            {
                'book_name': book.Book.name,
                'user': book.User.username,
                'issue_date': book.BorrowedBooks.issue_date.strftime('%Y-%m-%d'),
                'due_date': book.BorrowedBooks.due_date.strftime('%Y-%m-%d')
            }
            for book in overdue_books_data
        ],
        'books_by_section': [
            {
                'section': section if section is not None else 'Unknown',
                'count': count
            }
            for section, count in books_by_section
        ]
    }

    message = format_message('templates/monthly_report.html', data=data)

    send_email(
        "libraraian@gmail.com",
        subject="Monthly Activity Report",
        message=message,
        content="html"
    )
