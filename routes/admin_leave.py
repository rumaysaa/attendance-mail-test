from flask import Blueprint,render_template,session,jsonify,request, url_for,redirect

bp = Blueprint('adm_leave',__name__,)

from modules.Admin_leave import *


@bp.route('/',methods=['get'])
def leave():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    month=(request.args.get('month'))
    year=(request.args.get('year'))
    if(month == None):
        month =datetime.now().month
        year = datetime.now().year
    data = getLeaves(int(month),int(year))
    return render_template('admin_leave.html',leaves=data)

@bp.route('/update_leave_status',methods=['post'])
def updateLeave():
    leaveID = request.json['leaveID']
    status = request.json['status']
    employee_email = request.json['employee_email']
    apply_date = request.json['apply_date']
    msg = request.json['msg']
    updated = updateLeaveStatus(leaveID,status,employee_email,apply_date,msg)
    #print(updated)
    return {"response": "updated"}
