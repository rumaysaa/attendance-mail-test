from flask import Blueprint,render_template,session,redirect,request
from modules.Account import getAccountDetails
from modules.Dashboard import getHeaderInfo
from modules.Admin_noti import *
from modules.Admin_holidays import getHolidayDetails
from modules.Admin_events import getEventDetails
bp = Blueprint('noti',__name__,)

@bp.route('/', methods=['get'])
def noti():
    empID = session.get("employee_id")
    if(empID == None):
        return redirect('/auth/login')
    data = getAccountDetails(empID)
    header_info = getHeaderInfo(data['fname'])
    notifications = getNotificationDetails()
    no_noti = count_read_noti(empID)
    no_holi =  len(getHolidayDetails())
    no_event = len(getEventDetails())
    return render_template('index.html',header_info=header_info,notis=notifications,acc_data=data ,page='notifications.html',no_noti=no_noti,no_holi=no_holi,no_event=no_event,empID=empID)

@bp.route('/mark_noti_as_read',methods=['post'])
def mark_noti():
    noti_id = request.json.get('id')
    empID = request.json.get('empID')
    status = markEmpAsRead(empID,noti_id)
    #print(status)
    return {"status":status}