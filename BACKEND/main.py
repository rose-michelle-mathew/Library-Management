
from applications.config import Config
from applications.model import User, Role
from applications.database import db
from applications.user_datastore import user_datastore

from flask_restful import Api
from flask_security import Security, SQLAlchemySessionUserDatastore, hash_password
from flask import Flask
from flask_cors import CORS

from applications import cache
from applications.workers import celery_init_app
from applications import task
from applications.cache import init_app

from applications.charts_api import charts_bp  

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config) ## send configurations of app
    db.init_app(app)   ##database initialization

    api = Api(app, prefix ='/api/v1')  ## created instance of API

    # user_datastore = SQLAlchemySessionUserDatastore(db.session,User,Role)  ##set up user datastore that will help in authentication - commented to remove circular import errors 
    app.security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()  ##creates sqlite databse for all the models we have defined

        ## populates these values to our database when the app is run for the first time
        librarian = app.security.datastore.find_or_create_role(name='librarian',description='Librarian')
        user = app.security.datastore.find_or_create_role(name='user',description = 'Members')
        if not app.security.datastore.find_user(email="librarian@gmail.com"): ## does the admin exist? then we don not create else we create a new admin 
            app.security.datastore.create_user(email="librarian@gmail.com", username='librarian', password=hash_password("password"),roles = [librarian])
        db.session.commit()

    return app,  api

app, api = create_app() 
cache.init_app(app)


celery_app =celery_init_app(app)
app.register_blueprint(charts_bp)

CORS(app)

from applications.auth_api import Login, Register, Logout

api.add_resource(Login,'/login') 
api.add_resource(Register,'/register')
api.add_resource(Logout,'/logout')

from applications.section_management_api import AllSections,AllBooks, Sections,Books,BookRequests, ApproveRejectRequest, UserHistory, RevokeAccess, Search, DownloadCSV
api.add_resource(AllSections,'/get_all_sections')
api.add_resource(Sections,'/add_section','/delete_section/<int:id>','/edit_section/<int:id>','/section/<int:id>')
api.add_resource(Books,'/add_book','/edit_book/<int:id>','/delete_book/<int:id>')
api.add_resource(AllBooks,'/section/<int:id>/get_all_books')
api.add_resource(BookRequests,'/request_book','/requests','/return','/revoke_book/<int:request_id>')
api.add_resource(ApproveRejectRequest,'/approvals','/borrowedBooks')
api.add_resource(UserHistory, '/history')
api.add_resource(RevokeAccess, '/revoke_access/<int:borrowed_id>')
api.add_resource(Search, '/search')
api.add_resource(DownloadCSV,'/download-csv')

from celery.schedules import crontab
from applications.task import check_and_send_reminders, send_monthly_activity_report


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule daily reminder task at 9:30
    sender.add_periodic_task(
        crontab(hour=15, minute=14),
        check_and_send_reminders.s(),
    )
    
    # Schedule monthly report task on the first day of every month
    sender.add_periodic_task(
        crontab(day_of_month=11, hour=14, minute=59),
        send_monthly_activity_report.s(),
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)