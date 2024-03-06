from flask import Flask,request,render_template,redirect,session,jsonify
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
from datetime import datetime,timedelta


#importing modules 
from modules.Dashboard import *

#importing routes
from routes.auth import bp as auth_bp
from routes.dashboard import bp as dash_bp
from routes.account import bp as acc_bp
from routes.events import bp as events_bp
from routes.notifications import bp as noti_bp
from routes.holidays import bp as holidays_bp
from routes.admin_dashboard import bp as adm_dash
from routes.admin_users import bp as adm_users
from routes.admin_projects import bp as adm_projs
from routes.admin_noti import bp as adm_noti
from routes.admin_holidays import bp as adm_holidays
from routes.admin_events import bp as adm_events
from routes.leave import bp as leave
from routes.admin_leave import bp as adm_leave
from routes.admin_tasks import bp as adm_tasks



#config app
app = Flask(__name__)
app.secret_key = "27eduCBA09"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=24)


#registering bluprints for the routes
app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(acc_bp,url_prefix='/account')
app.register_blueprint(dash_bp,url_prefix='/')
app.register_blueprint(events_bp,url_prefix='/events')
app.register_blueprint(noti_bp,url_prefix='/notifications')
app.register_blueprint(holidays_bp,url_prefix='/holidays')
app.register_blueprint(adm_dash,url_prefix='/admin')
app.register_blueprint(adm_users,url_prefix='/admin/users')
app.register_blueprint(adm_projs,url_prefix='/admin/projects')
app.register_blueprint(adm_noti,url_prefix='/admin/notifications')
app.register_blueprint(adm_holidays,url_prefix='/admin/holidays')
app.register_blueprint(adm_events,url_prefix='/admin/events')
app.register_blueprint(leave,url_prefix='/leave')
app.register_blueprint(adm_leave,url_prefix='/admin/leave')
app.register_blueprint(adm_tasks,url_prefix='/admin/tasks')



    
if __name__ == "__main__":
    app.run(host='localhost', port=3000,debug=True)
