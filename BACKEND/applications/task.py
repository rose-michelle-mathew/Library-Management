from collections import defaultdict
import csv
from datetime import datetime, timedelta
import os
from flask_mail import Mail, Message
from flask import Flask
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
            sender="librarian@library.com",
            recipients=[email]
        )
        msg.body = message
        mail.send(msg)
        return f"Email sent to {email}"


@shared_task(ignore_result=False)
def send_monthly_activity_report():
    today = datetime.today()
    first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)

    issued_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.issue_date >= first_day_of_last_month,
        BorrowedBooks.issue_date <= last_day_of_last_month
    ).all()

    overdue_books_data = db.session.query(BorrowedBooks, Book, User).join(Book).join(User).filter(
        BorrowedBooks.due_date < today
    ).all()

    books_by_section = db.session.query(
        Section.section_name, func.count(AllActivity.id)
    ).select_from(AllActivity).join(Book, AllActivity.book_id == Book.id).join(Section, Book.section_id == Section.id).filter(
        AllActivity.status == 'borrowed',
        AllActivity.requested_date >= first_day_of_last_month,
        AllActivity.requested_date <= last_day_of_last_month
    ).group_by(Section.section_name).all()

    new_books_data = db.session.query(Book, Section).join(Section).filter(
        Book.date_created >= first_day_of_last_month,
        Book.date_created <= last_day_of_last_month
    ).all()

    new_sections_data = db.session.query(
        Section, func.count(Book.id).label('book_count')
    ).outerjoin(Book).filter(
        Section.date_created >= first_day_of_last_month,
        Section.date_created <= last_day_of_last_month
    ).group_by(Section.id).all()

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
        ],
        'new_books': [
            {
                'book_name': book.Book.name,
                'date_created': book.Book.date_created.strftime('%Y-%m-%d'),
                'section': book.Section.section_name
            }
            for book in new_books_data
        ],
        'new_sections': [
            {
                'section_name': section.Section.section_name,
                'date_created': section.Section.date_created.strftime('%Y-%m-%d'),
                'book_count': section.book_count
            }
            for section in new_sections_data
        ]
    }

    message = format_message('templates/monthly_report.html', data=data)

    send_email(
        "libraraian@gmail.com",
        subject="Monthly Activity Report",
        message=message,
        content="html"
    )

@shared_task(ignore_result=False)
def export_all_activity_to_csv():
    # Calculate the first and last day of the previous month
    today = datetime.today()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    
    # Query AllActivity with joins to Book and User for the previous month
    activity_data = db.session.query(
        AllActivity,
        Book.name.label('book_name'),
        User.username.label('username')
    ).join(Book, AllActivity.book_id == Book.id) \
     .join(User, AllActivity.user_id == User.id) \
     .filter(
         AllActivity.requested_date >= first_day_of_last_month,
         AllActivity.requested_date <= last_day_of_last_month
     ).all()
    
    directory = "/home/michelle/Reports/"
    os.makedirs(directory, exist_ok=True) 
    csv_file_path = os.path.join(directory, f"activity_report_{first_day_of_last_month.strftime('%m-%Y')}.csv")

    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        
        csvwriter.writerow(["ID", "Book Name", "Username", "Requested Date", "Approved Date", "Status"])
        
        for record in activity_data:
            activity, book_name, username = record
            csvwriter.writerow([
                activity.id,
                book_name,
                username,
                activity.requested_date.strftime('%Y-%m-%d %H:%M:%S'),
                activity.approved_date.strftime('%Y-%m-%d %H:%M:%S'),
                activity.status
            ])
            
    send_completion_alert(csv_file_path)
    print(f"CSV export completed: {csv_file_path}")

@shared_task(ignore_result=False)
def send_completion_alert(file_path):
    with app.app_context():  
        subject = "Batch Job Completed"
        recipient_email = "librarian@gmail.com"
        
        msg = Message(
            subject=subject,
            sender="noreply@library.com",
            recipients=[recipient_email]
        )
        msg.body = f"The batch job has completed successfully. The report is available at {file_path}."
        
        mail.send(msg)
        
        return f"Email sent to {recipient_email} with file path {file_path}"
