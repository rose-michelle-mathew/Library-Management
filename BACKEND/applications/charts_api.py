from flask import Blueprint, jsonify, make_response
from flask_login import current_user
from sqlalchemy import func
from applications.cache import cache
from applications.database import db
from applications.model import *
charts_bp = Blueprint('charts', __name__)

@charts_bp.route('/api/v1/most-borrowed-books', methods=['GET'])
def most_borrowed_books():
    books = db.session.query(
        Book.name,  
        db.func.count(AllActivity.book_id).label('borrowed_count')
    ).join(
        AllActivity,  
        Book.id == AllActivity.book_id  
    ).filter(
        AllActivity.status == 'borrowed'  
    ).group_by(
        Book.name  
    ).order_by(
        db.func.count(AllActivity.book_id).desc()  
    ).limit(5).all()  

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
def get_active_users():
    colors = ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.6)',
              'rgba(255, 206, 86, 0.7)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)']
    active_users_data = db.session.query(
        func.count(UserLogins.user_id).label('user_id'),
        User.username).join(User, UserLogins.user_id == User.id).filter(User.username != "librarian")\
     .group_by(User.username)\
        .limit(5).all()

  
    response_data = {
        'labels': [username for _, username in active_users_data],
        'datasets': [{
            'data': [count for count, _ in active_users_data],
            'backgroundColor': colors
        }]
    }

    return jsonify(response_data)

@charts_bp.route('/api/v1/popular-sections', methods=['GET'])
def popular_sections():
   
    sections = db.session.query(
        Section.section_name,
        db.func.count(Book.id).label('total_books_in_section')
    ).join(
        Book, Section.id == Book.section_id
    ).group_by(
        Section.section_name
    ).subquery()

   
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

    
    combined = db.session.query(
        sections.c.section_name,
        sections.c.total_books_in_section,
        db.func.coalesce(borrowed_books.c.borrowed_books_in_section, 0).label('borrowed_books_in_section')
    ).outerjoin(
        borrowed_books, sections.c.section_name == borrowed_books.c.section_name
    ).order_by(
        sections.c.total_books_in_section.desc()  
    ).limit(5).all()

   
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

@charts_bp.route('/api/v1/borrowed-books-by-section', methods=['GET'])
def get_borrowed_books_by_section():
    user_id = current_user.id

    section_counts = db.session.query(
        Section.section_name,
        func.count(AllActivity.id)
    ).join(Book, AllActivity.book_id == Book.id)\
     .join(Section, Book.section_id == Section.id)\
     .filter(AllActivity.user_id == user_id, AllActivity.status == 'borrowed')\
     .group_by(Section.section_name)\
     .order_by(func.count(AllActivity.id).desc())\
     .limit(5).all()
    
    colors = ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.6)',
              'rgba(255, 206, 86, 0.7)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)']
# Prepare data for chart
    section_data = {
        'labels': [section_name for section_name, _ in section_counts],
        'datasets': [{
            'label': 'Books by section',
            'data': [count for _, count in section_counts],
            'backgroundColor': colors[:len(section_counts)],  
            'borderColor': colors[:len(section_counts)],      
            'borderWidth': 1
        }]
    }

    return make_response(jsonify(section_data), 200)

@charts_bp.route('/api/v1/recent-user-activity', methods=['GET'])
@cache.cached(timeout=50)

def get_recent_user_activity():
    user_id = current_user.id

    activities = db.session.query(
        func.strftime('%Y-%m', AllActivity.requested_date).label('month'),
        AllActivity.status,
        func.count(AllActivity.id)
    ).filter(AllActivity.user_id == user_id).group_by(func.strftime('%Y-%m', AllActivity.requested_date), AllActivity.status)\
     .order_by(func.strftime('%Y-%m', AllActivity.requested_date), AllActivity.status).all()

    status_data = {}
    for month, status, count in activities:
        if status not in status_data:
            status_data[status] = {'months': [], 'counts': []}
        status_data[status]['months'].append(month)
        status_data[status]['counts'].append(count)

    all_months = sorted(set(month for month, _, _ in activities))
    response_data = {
        'labels': all_months,
        'datasets': []
    }

    colors = ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.7)', 'rgba(75, 192, 192, 0.6)','rgba(255, 206, 86, 0.7)','rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)']
    for (status, color) in zip(status_data.keys(), colors):
        dataset = {
            'label': status,
            'data': [status_data[status]['counts'][status_data[status]['months'].index(month)] if month in status_data[status]['months'] else 0 for month in all_months],
            'borderColor': color,
            'backgroundColor': color,
            'fill': False
        }
        response_data['datasets'].append(dataset)
    
    return jsonify(response_data)