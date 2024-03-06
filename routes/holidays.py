from flask import Blueprint,render_template,session,redirect

from modules.Admin_holidays import getHolidayDetails
from modules.Account import getAccountDetails
from modules.Dashboard import getHeaderInfo
from modules.Admin_noti import *
from modules.Admin_events import getEventDetails
bp = Blueprint('holidays',__name__,)

@bp.route('/',methods=['get'])
def holidays():
    empID = session.get("employee_id")
    if(empID == None):
        return redirect('/auth/login')
    data = getAccountDetails(empID)
    header_info = getHeaderInfo(data['fname'])
    holidays =  getHolidayDetails()
    no_holi = len(holidays)
    no_noti = count_read_noti(empID)
    no_event = len(getEventDetails())
    return render_template('index.html',header_info=header_info,acc_data=data ,page='holidays.html',holidays=holidays,no_noti=no_noti,no_holi=no_holi,no_event=no_event)

