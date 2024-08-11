from flask_login import current_user
from applications.user_datastore import user_datastore
from flask_restful import Resource
from flask import make_response, jsonify, request
from flask_security import utils, auth_token_required
from applications.model import *


class Login(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')

        if not email or not password:
            return make_response(jsonify({'message':'Email and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message':'Invalid Credentials - User doesn\'t exists '}),401)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message':'Invalid Credentials - Invalid Password'}),401)

        utils.login_user(user)
        auth_token = user.get_auth_token()

        login_entry = UserLogins(user_id=user.id)
        db.session.add(login_entry)
        db.session.commit()

        response = {
            'message':'Login Successful',
            'user':{
                'username':user.username,
                'email':user.email,
                'address' : user.address,
                'roles': [role.name for role in user.roles],
                'auth_token':auth_token
            }
        } 
        return make_response(jsonify(response),200) 
    
class Register(Resource):
    def post(self):
        recieved_data = request.get_json()

        username = recieved_data.get('username')
        email = recieved_data.get('email')
        password = recieved_data.get('password')
        address = recieved_data.get('address')
        role   = recieved_data.get('role')

        if not email or not password or not username:
            return make_response(jsonify({'message':'Email and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'message':'User with email already exists'}),401)
        
        user = user_datastore.find_user(username=username)
        if user:
            return make_response(jsonify({'message':'Username already exists'}),401)
        
        if '@' not in email or '.' not in email:
            return make_response(jsonify({'message':'Invalid Email'}),400)
        
        if len(password) < 8:
            return make_response(jsonify({'message':'Password must be atleast 8 characters long'}),400)
        
        if len(username) < 3 or not username.isalnum():
            return make_response(jsonify({'message':'Username must be atleast 3 characters long and alphanumeric characters'}),400)

        if role not in ['user']:
            return make_response(jsonify({'message':'Invalid Role'}),400)
        
        try:
            user =user_datastore.create_user(email=email,username=username,address=address,password=utils.hash_password(password),roles=[role])
            user_datastore.commit()

            response = {
                'message':'User Registered Successfully',
                'user':{
                    'username':user.username,
                    'roles': [role.name for role in user.roles],
                }
            } 
            return make_response(jsonify(response),200) 
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),500)
        
class Logout(Resource):
    @auth_token_required 
    def post(self):
        user = current_user

        login_entry = UserLogins.query.filter_by(user_id=user.id).order_by(UserLogins.login_time.desc()).first()
        if login_entry and not login_entry.logout_time:
            login_entry.logout_time = datetime.utcnow()
            db.session.commit()

        utils.logout_user()

        return make_response(jsonify({'message': 'Logout Successful'}), 200)

        
        



        