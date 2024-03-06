from flask import Blueprint,render_template,session,redirect,url_for,request,jsonify,request
bp = Blueprint('dash',__name__,)
import os
from modules.Dashboard import *
from modules.Account import getAccountDetails
from datetime import datetime
from modules.Frs import *
from modules.Admin_noti import *
from modules.Admin_holidays import getHolidayDetails
from modules.Admin_events import getEventDetails
#-------Client--------
#---gets
@bp.route('/checkin', methods=['get','post'])
def checkin():
    empID = session.get("employee_id")
    if(empID == None):
        return redirect('/auth/login')
    inoffice = request.json['inoffice']
    res = insertEmployeeCheckin(empID,inoffice)
    session["indiv_att"].append(res)
    session["current_att_id"] = res["id"]
    return jsonify(res)

@bp.route('/', methods=['get','post'])
def index():
    #print(request.remote_addr)
    empID = session.get("employee_id")
    page = 'dashboard.html'
    if(empID == None):
        return redirect('/auth/login')
    json = getSingleEmployeeAttendance(empID)
    session["indiv_att"] = json
    out_btn = False
    in_btn = True
    if(len(json)!=0):
        if(json[0]["out"] == None):
            in_btn = False
            out_btn = True
        elif(json[0]["out"] != None):
            in_btn = True
            out_btn = False
    current_record_id = None
    if(session.get("current_att_id")!= None ):
        current_record_id = session["current_att_id"]
    elif(len(json) != 0 and session.get("current_att_id") == None):
        #print(session.get("indiv_att"))
        current_record_id = str(session["indiv_att"][0]["id"])
    all_att = getAllEmployeesAttendance()
    try:
        quote = getRandomQuote().partition('—')
    except:
        return redirect(url_for('.index'))
    projects = getProjectsByEmp(empID)
    emp_name = getAccountDetails(empID)["fname"]
    header_info = getHeaderInfo(emp_name)
    account_details = getAccountDetails(empID)
    no_noti = count_read_noti(empID)
    no_holi = len( getHolidayDetails())
    no_event = len(getEventDetails())
    return render_template('index.html',header_info=header_info,acc_data=account_details,cin = in_btn,cou=out_btn,record_id=current_record_id,page=page,all_att=all_att,quote=quote,proj=projects,no_noti=no_noti,no_holi=no_holi,no_event=no_event)

@bp.route('/working_hr_count',methods=['get'])
def count_working_hr():
    empID = session.get("employee_id")
    data = list(db.Attendance.find( {
    "date" : datetime.fromisoformat(date.today().isoformat()),
    "employeeID" : ObjectId(empID)
    }).sort('checkInTime', pymongo.DESCENDING))
    if(len(data) != 0 ):
        if data[0]['checkOutTime'] == None:
            in_ = data[0]['checkInTime']
            curr = datetime.now()
            diff =  (str((curr - in_)).split(".")[0])
            return jsonify({"hr": diff.split(':')})
    return jsonify({"hr": ['00','00','00']})

@bp.route('/frs',methods=['post'])
def frs():
    video = request.files['video']
    #print(video)
    empID = session.get("employee_id")
    path = './static/video/'+empID+'.webm'
    #print(os.path.exists(path))
    video.save(path)
    status = verify_faces(empID,path)
    #print(status)
    os.remove(path)
    return jsonify({"status_":str(status)})##status}
#--posts
@bp.route('/checkout', methods=['post'])
def checkout():
    empID = session.get("employee_id")
    stamp_id = request.json['id']
    if(empID == None):
        return redirect('/auth/login')
    res = updateEmployeeCheckout(stamp_id,empID)
    session["current_att_id"] = None
    return jsonify(res)

@bp.route('/task_report',methods=['post'])
def task_report():
    #print(request.json)
    empID = session.get("employee_id")
    #print(empID)
    projID = request.json.get("projectID")
    task_type = request.json.get("task_type")
    task_detail = request.json.get("desc")
    db.Tasks.insert_one({
        "projectID" : ObjectId(projID),
        "employeeID": ObjectId(empID),
        "date": datetime.now(),
        "task_type" : task_type,
        "task_detail": task_detail
    })
    #print()
    return "true"


