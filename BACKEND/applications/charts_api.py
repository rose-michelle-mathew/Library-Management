from flask import Blueprint, jsonify, make_response
from applications.database import db
from applications.model import *
charts_bp = Blueprint('charts', __name__)

@charts_bp.route('/api/v1/most-borrowed-books', methods=['GET'])
def most_borrowed_books():
    # Query the all_activity table to get the most borrowed books where the status is 'borrowed'
    books = db.session.query(
        Book.name,  # Assuming the Book model has a 'name' attribute
        db.func.count(AllActivity.book_id).label('borrowed_count')
    ).join(
        AllActivity,  # Join with the AllActivity table
        Book.id == AllActivity.book_id  # Assuming 'book_id' is the foreign key in AllActivity
    ).filter(
        AllActivity.status == 'borrowed'  # Filter for status 'borrowed'
    ).group_by(
        Book.name  # Group by book name
    ).order_by(
        db.func.count(AllActivity.book_id).desc()  # Order by borrow count
    ).limit(5).all()  # Limit to top 5 most borrowed books

    data = {
        'labels': [book_name for book_name, _ in books],
        'datasets': [{
            'label': 'Borrow Count',
            'data': [borrowed_count for _, borrowed_count in books],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': '#FF6384',
            'borderWidth': 3
        }]
    }
    return make_response(jsonify(data), 200)


@charts_bp.route('/api/v1/popular-authors', methods=['GET'])
def popular_authors():
    authors = db.session.query(Book.authors, db.func.count(Book.id).label('book_count'))\
        .group_by(Book.authors)\
        .order_by(db.func.count(Book.id).desc())\
        .limit(5)\
        .all()

    data = {
        'labels': [author for author, _ in authors],
        'datasets': [{
            'label': 'Number of Books',
            'data': [count for _, count in authors],
            'backgroundColor': 'rgba(66, 165, 245, 0.2)',
            'borderColor': '#42A5F5',
            'borderWidth': 3
        }]
    }
    return make_response(jsonify(data),201)

@charts_bp.route('/api/v1/active-users', methods=['GET'])
def active_users():
    users = db.session.query(User.username, db.func.count(UserLogins.id).label('login_count'))\
        .join(UserLogins, User.id == UserLogins.user_id)\
        .group_by(User.username)\
        .order_by(db.func.count(UserLogins.id).desc())\
        .limit(5)\
        .all()

    data = {
        'labels': [username for username, _ in users],
        'datasets': [{
            'label': 'Login Count',
            'data': [count for _, count in users],
            'backgroundColor': 'rgba(66, 165, 245, 0.2)',
            'borderColor': '#42A5F5',
            'borderWidth': 1
        }]
    }
    return make_response(jsonify(data),201)

@charts_bp.route('/api/v1/popular-sections', methods=['GET'])
def popular_sections():
    # Query the count of books in each section
    sections = db.session.query(
        Section.section_name,
        db.func.count(Book.id).label('total_books_in_section')
    ).join(
        Book, Section.id == Book.section_id
    ).group_by(
        Section.section_name
    ).subquery()

    # Query the count of borrowed books in each section
    borrowed_books = db.session.query(
        Section.section_name,
        db.func.count(BorrowedBooks.id).label('borrowed_books_in_section')
    ).join(
        Book, BorrowedBooks.book_id == Book.id
    ).join(
        Section, Book.section_id == Section.id
    ).filter(
        BorrowedBooks.status == 'borrowed'
    ).group_by(
        Section.section_name
    ).subquery()

    # Combine both queries
    combined = db.session.query(
        sections.c.section_name,
        sections.c.total_books_in_section,
        db.func.coalesce(borrowed_books.c.borrowed_books_in_section, 0).label('borrowed_books_in_section')
    ).outerjoin(
        borrowed_books, sections.c.section_name == borrowed_books.c.section_name
    ).order_by(
        sections.c.total_books_in_section.desc()  # Corrected ordering
    ).limit(5).all()

    # Prepare the data for the chart
    data = {
        'labels': [row.section_name for row in combined],
        'datasets': [
            {
                'label': 'Total Books in Section',
                'data': [row.total_books_in_section for row in combined],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': '#36A2EB',
                'borderWidth': 2
            },
            {
                'label': 'Borrowed Books in Section',
                'data': [row.borrowed_books_in_section for row in combined],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': '#FF6384',
                'borderWidth': 2
            }
        ]
    }

    return make_response(jsonify(data), 200)

