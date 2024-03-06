from flask import Blueprint,render_template,redirect,jsonify,request,session
from modules.Admin_noti import *

bp = Blueprint('adm_noti',__name__,)
from datetime import timedelta,datetime

@bp.route('/',methods=['get'])
def adm_notis():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    notifications = getNotificationDetails()
    #print(notifications)
    return render_template('admin_notifications.html',notis=notifications)

@bp.route('/create',methods=['post'])
def create_notis():
    #(request.json)
    noti = createNotification(dict(request.json))
    if(noti != None):
        return "true"
    else:
        return "false"
    
@bp.route('/delete',methods=['get'])
def delete_adm_notis():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    noti_id = request.args.get("id")
    deleted = deleteNotificationById(noti_id)
    #print(deleted)
    return redirect('/admin/notifications/')