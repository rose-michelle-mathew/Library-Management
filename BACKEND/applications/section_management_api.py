from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from applications.model import *
from applications.marshall_fields import *
from datetime import datetime,timedelta


class AllSections(Resource):

## To obtain all the sections in the Database, User and Librarian can view
    @marshal_with(section)
    def get(self):
        sections = Section.query.all()
        return sections
    
class Sections(Resource):
    
    ### To add a new section to the database, only librarian can add

    @marshal_with(section)
    def get(self, id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message':'Section not FOund'}),404)
        return section



    @auth_token_required
    @roles_required('librarian')
    def post(self):
        data = request.get_json()

        section_name = data.get('section_name')
        description = data.get('description')
        date_created = data.get('date_created')

        try:
            date_created = datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
           return jsonify({"error": str(e)}), 400

        if not section_name:
            return make_response(jsonify({'message':'Section Name is Required'}),400)
        
        if Section.query.filter_by(section_name=section_name).first():
            return make_response(jsonify({'message':'Section Name already exists'}),400)
        
        try:
            section = Section(section_name=section_name,description=description,date_created=date_created)
            db.session.add(section)
            db.session.commit()
            return make_response(jsonify({'message':'Section added Successfully'}),201)
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('librarian')
    def delete(self,id):
        section = Section.query.get(id)

        if not section:
                return make_response(jsonify({"message":"Section Does not exist"}),404)
        
        try:
            db.session.delete(section)
            db.session.commit()
            return make_response(jsonify({'message':'Section deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

        
    @auth_token_required
    @roles_required('librarian')
    def put(self, id):

        section = Section.query.get(id)

        if not section:
            return make_response(jsonify({"message":"Section  not found"}),400)
        
        data = request.get_json()

        section_name = data.get('section_name')
        description =data.get('description')

        if not section_name and not description:
            return make_response(jsonify({"message":"Edit request is empty"}),400)
        
        if section_name:
            section.section_name = section_name
        if description:
            section.description = description
        try:
            db.session.commit()
            return make_response(jsonify({"message":"Section Edited Successfully"}),201)
        except Exception as e:
            return make_response(jsonify({"message":str(e)}),404)
        
class AllBooks(Resource):
    def get(self,id):
        books = Book.query.filter_by(section_id=id).all()
        if not books:
            return make_response(jsonify({"message":"No books exist"}),400)
 
        response = []
        for book in books:
            section = Section.query.get(book.section_id)
            response.append({
                'book_id':book.id,
                'name':book.name,
                'description':book.content,
                'authors':book.authors,
                'section':{
                    'sectionid':section.id,
                    'name':section.section_name,
                    'description':section.description
                }
            })
        return make_response(jsonify(response),200)
    
        
class Books(Resource):
    
    ### adding a new book to the db, only restriced to librarian 
    @auth_token_required
    @roles_required('librarian')
    def post(self):
        data = request.get_json()

        book_name = data.get('book_name')
        content =data.get('content')
        authors = data.get('authors')
        # date_issued = data.get('date_issued')
        # return_date = data.get('return_date')
        section_name = data.get('section_name')
        section_id = data.get('section_id')

        section = Section.query.filter_by(section_name =section_name).first()

        if not section:
            return make_response(jsonify({"message":"Section Does not exist"}),400)

        if not book_name or not content or not authors or not section_name:
            return make_response(jsonify({"message":"Fields must not be empty"}),400)
        
        if Book.query.filter_by(name=book_name, section_id=section.id).first():
            return make_response(jsonify({'message': 'Book already exists in this section'}), 400)
       
        try:
            book = Book(name=book_name,content=content,authors=authors,section_id=section.id)
            db.session.add(book)
            db.session.commit()
            response = {
                'message':'Book added successfully',
                'book':{
                    'book_id':book.id,
                    'name':book.name,
                    'description':book.content,
                    'section_id':book.section_id
                }
            }
            return make_response(jsonify(response),201)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('librarian')
    def put(self, id):

        book = Book.query.get(id)

        if not book:
            return make_response(jsonify({"message":"Book  not found"}),400)
        
        data = request.get_json()

        book_name = data.get('book_name')
        content =data.get('content')
        authors = data.get('authors')
        # date_issued = data.get('date_issued')
        # return_date = data.get('return_date')
        section_name = data.get('section_name')
        section_id = data.get('section_id')

        if not book_name or not content or not authors or not section_name:
            return make_response(jsonify({"message":"Edit request is empty"}),400)
        
        if book_name:
            book.name = book_name
        if content:
            book.content = content
        if authors:
            book.authors = authors
        if section_name:
            section = Section.query.filter_by(section_name= section_name).first()
            if not section:
                return make_response(jsonify({"message":"Section Name Does not exist"}),404)
            book.section_name = section_name
        if section_id:
            section = Section.query.filter_by(id= section_id).first()
            if not section:
                return make_response(jsonify({"message":"Section ID Does not exist"}),404)
            book.section_id = section_id
        
        try:
            db.session.commit()
            return make_response(jsonify({"message":"Book Edited Successfully"}),201)
        except Exception as e:
            return make_response(jsonify({"message":str(e)}),404)
        
    @auth_token_required
    @roles_required('librarian')
    def delete(self,id):
        book = Book.query.get(id)

        if not book:
                return make_response(jsonify({"message":"Book Does not exist"}),404)
        
        try:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message':'Book deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
        
class BookRequests(Resource):
    
    @auth_token_required
    @roles_required('user')
    def post(self):
        data = request.get_json()

        book_name = data.get('book_name')
        section_name = data.get('section_name')
        user_id = current_user.id  

        # Check if the user has reached the request limit (5 requests)
        user_request_count = Request.query.filter_by(user_id=user_id).count()
        if user_request_count >= 5:
            return make_response(jsonify({'message': 'You have reached the maximum limit of requests (5)'}), 400)

        # Find the book by book_name and section_name
        book = Book.query.join(Section).filter(Book.name == book_name, Section.section_name == section_name).first()

        if not book:
            return make_response(jsonify({'message': 'Book not found in the specified section'}), 404)

        # Check if the user has already requested this book
        existing_request = Request.query.filter_by(book_id=book.id, user_id=user_id).first()
        if existing_request:
            return make_response(jsonify({'message': 'You have already requested this book'}), 400)
        ### !!! Check If book is already borrowed by user
        already_borrowed = BorrowedBooks.query.filter_by(book_id=book.id, user_id=user_id).first()
        if already_borrowed:
            return make_response(jsonify({'message': 'You have already borrowed this book'}), 400)


        # Create a new request
        new_request = Request(book_id=book.id, user_id=user_id, status='Pending')  # Assuming status starts as Pending
        try:
            db.session.add(new_request)
            db.session.commit()
            return make_response(jsonify({'message': 'Book request added successfully'}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)
        

    @auth_token_required
    @roles_required('user')
    def put(self):
        data = request.get_json()
        borrowed_id = data.get('borrowed_id')

        # Fetch the borrowed book by id
        borrowed_book = BorrowedBooks.query.filter_by(id=borrowed_id, user_id=current_user.id).first()
        if not borrowed_book or borrowed_book.status != 'borrowed':
            return make_response(jsonify({"message": "You have not borrowed this book"}), 400)

        # Update AllActivity to mark as returned
        activity_log = AllActivity(
            user_id=current_user.id,
            book_id=borrowed_book.book_id,
            requested_date=borrowed_book.issue_date,
            approved_date=datetime.utcnow(),
            status='returned'
        )
        try:
            db.session.add(activity_log)
            db.session.delete(borrowed_book)  # Remove the borrowed entry
            db.session.commit()
            return make_response(jsonify({"message": "Book returned successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": str(e)}), 400)


    @auth_token_required
    def get(self):
        if current_user.has_role('librarian'):
            # Librarian view: Retrieve all requests
            requests = Request.query.all()
        else:
            # Regular user view: Retrieve only user's requests
            user_id = current_user.id
            requests = Request.query.filter_by(user_id=user_id).all()

        response = []
        for req in requests:
            book = Book.query.get(req.book_id)
            section = Section.query.get(book.section_id)
            user = User.query.filter_by(id=req.user_id).first()
            user_name = user.username if user else 'Unknown'
            response.append({
                'request_id': req.id,
                'book': {
                    'book_id': book.id,
                    'name': book.name,
                    'description': book.content,
                    'authors': book.authors,
                    'section': {
                        'section_id': section.id,
                        'name': section.section_name,
                        'description': section.description
                    }
                },
                'user_id': req.user_id,
                'user_name': user_name,
                'status': req.status,
                'date_of_request': req.date_of_request.strftime('%Y-%m-%d')
            })

        return make_response(jsonify(response), 200)


    
            
    @auth_token_required
    @roles_required('user')

    def delete(self, request_id):
        # Check if the request exists
        book_request = Request.query.get(request_id)
        if not book_request:
            return make_response(jsonify({'message': 'Request not found'}), 404)

        try:
            db.session.delete(book_request)
            db.session.commit()
            return make_response(jsonify({'message': 'Request revoked successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


class ApproveRejectRequest(Resource):
    @auth_token_required
    @roles_required('librarian')

    def put(self):
        data = request.get_json()
        request_id = data.get('request_id')
        action = data.get('action')
        # action should be 'approve' or 'reject'

        # Fetch the request by ID
        book_request = Request.query.get(request_id)
        if not book_request:
            return make_response(jsonify({"message": "Request not found"}), 404)

        if action == 'approve':
            # Approve the request and add to ActivityLog and BorrowedBooks
            issue_date = datetime.utcnow()
            due_date = issue_date + timedelta(days=7)  # Assuming a 7-day borrowing period
            borrowed_book = BorrowedBooks(
                user_id=book_request.user_id,
                book_id=book_request.book_id,
                issue_date=issue_date,
                due_date=due_date,
                status='borrowed'
            )
            db.session.add(borrowed_book)

            activity_log = AllActivity(
                user_id=book_request.user_id,
                book_id=book_request.book_id,
                requested_date=book_request.date_of_request,
                approved_date=issue_date,
                status='borrowed'
            )
            db.session.add(activity_log)

            db.session.delete(book_request)
            db.session.commit()

            return make_response(jsonify({"message": "Request approved and book borrowed"}), 200)

        elif action == 'reject':
            # Reject the request and add to ActivityLog
            activity_log = AllActivity(
                user_id=book_request.user_id,
                book_id=book_request.book_id,
                requested_date=book_request.date_of_request,
                approved_date=datetime.utcnow(),
                status='rejected'
            )
            db.session.add(activity_log)

            db.session.delete(book_request)
            db.session.commit()

            return make_response(jsonify({"message": "Request rejected"}), 200)

        else:
            return make_response(jsonify({"message": "Invalid action"}), 400)


    @auth_token_required
    def get(self):

        if current_user.has_role('librarian'):
            # Librarian view: Retrieve all requests
            borrowed_books = BorrowedBooks.query.all()
        else:
            user_id = current_user.id
            borrowed_books = BorrowedBooks.query.filter_by(user_id=user_id).all()

        response = []
        for borrowed in borrowed_books:
            book = Book.query.get(borrowed.book_id)
            section = Section.query.get(book.section_id)
            user = User.query.get(borrowed.user_id)
            response.append({
                'borrowed_id': borrowed.id,
                'book': {
                    'book_id': book.id,
                    'name': book.name,
                    'description': book.content,
                    'authors': book.authors,
                    'section': {
                        'section_id': section.id,
                        'name': section.section_name,
                        'description': section.description
                    }
                },
                'user_id': borrowed.user_id,
                'user_name': user.username,  # Ensure this field exists in your User model
                'issue_date': borrowed.issue_date.strftime('%Y-%m-%d'),
                'due_date': borrowed.due_date.strftime('%Y-%m-%d'),
                'status': borrowed.status
            })

        return make_response(jsonify(response), 200)
    
class UserHistory(Resource):

    @auth_token_required
    @roles_required('user')
    def get(self):
        user_id = current_user.id

        # Fetch activity logs with status 'rejected' and 'returned'
        activity_logs = AllActivity.query.filter(AllActivity.user_id == user_id, AllActivity.status.in_(['rejected', 'returned'])).all()
        activity_response = []
        for activity in activity_logs:
            book = Book.query.get(activity.book_id)
            section = Section.query.get(book.section_id)
            activity_response.append({
                'activity_id': activity.id,
                'book': {
                    'book_id': book.id,
                    'name': book.name,
                    'description': book.content,
                    'authors': book.authors,
                    'section': {
                        'section_id': section.id,
                        'name': section.section_name,
                        'description': section.description
                    }
                },
                'requested_date': activity.requested_date.strftime('%Y-%m-%d'),
                'approved_date': activity.approved_date.strftime('%Y-%m-%d'),
                'status': activity.status
            })

        response = {
            'activity_logs': activity_response,
        }

        return make_response(jsonify(response), 200)
