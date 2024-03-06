from flask import Blueprint,render_template,redirect,jsonify,request,session
from modules.Admin_holidays import getHolidayDetails
from modules.Account import getAccountDetails
from modules.Dashboard import getHeaderInfo
from modules.Admin_noti import *
from modules.Admin_events import getEventDetails
from modules.Leave import *

bp = Blueprint('leave',__name__,)
from datetime import timedelta,datetime

@bp.route('/',methods=['get','post'])
def leave():
    empID = session.get("employee_id")
    if(empID == None):
        return redirect('/auth/login')
    leaves = getLeaveByEmpID(empID)
    #print(leaves)
    data = getAccountDetails(empID)
    header_info = getHeaderInfo(data['fname'])
    holidays =  getHolidayDetails()
    no_holi = len(holidays)
    no_noti = count_read_noti(empID)
    no_event = len(getEventDetails())
    return render_template('index.html',page='leave.html',header_info=header_info,acc_data=data,no_noti=no_noti,no_holi=no_holi,no_event=no_event,leaves=leaves)

@bp.route('/apply',methods=['get','post'])
def apply_leave():
    empID = session.get("employee_id")
    if(empID == None):
        return redirect('/auth/login')
    if(request.method=='POST'):
        leave = leaveApply(request.json)
    data = getAccountDetails(empID)
    header_info = getHeaderInfo(data['fname'])
    holidays =  getHolidayDetails()
    no_holi = len(holidays)
    no_noti = count_read_noti(empID)
    no_event = len(getEventDetails())
    return render_template('index.html',page='leave_apply.html',header_info=header_info,acc_data=data,no_noti=no_noti,no_holi=no_holi,no_event=no_event,empID=empID)