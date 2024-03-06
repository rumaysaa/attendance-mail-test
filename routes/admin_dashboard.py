
from flask import Blueprint,render_template,session,redirect,jsonify,request
from modules.Admin_dashboard import *
from modules.Dashboard import *
from modules.Account import getAccountDetails
bp = Blueprint('adm_dash',__name__,)
from datetime import timedelta,datetime

@bp.route('/',methods=['get'])
def admin():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    active_users_data = getActiveEmployees()
    active_users_no = len(active_users_data)
    active_users_names = [i['name'] for i in getActiveEmployees()]
    allEmp = list(db.Employees.find({
         "_id" : {"$ne": ObjectId("65d5c2bdb6fb19d2beb15375")}
    }))
    inactive_users =  getInactiveEmployees(allEmp,active_users_data)
    inactive_users_no = len(inactive_users)
    inactive_users_details =  [getAccountDetails(i) for i in inactive_users]
    inactive_users_names=[]
    for i in inactive_users_details:
        inactive_users_names.append(i['fname']+" "+i['lname'])
    outside_working_no = 0
    outside_working_names = []
    for i in active_users_data:
        if i['status']==False or i['status'] == "":
            outside_working_no +=1
            outside_working_names.append(i['name'])
    projects= getProjects()
    projects_no = len(projects)
    data = getAllEmployeesAttendance()
    present_users = getPresentEmployees()
    absent_employees = getAbsentEmployees(allEmp,present_users)
    absent_users_details =  [getAccountDetails(i) for i in absent_employees]
    return render_template('admin_dashboard.html',active_users_no=active_users_no,inactive_users_no=inactive_users_no,active_users_names=active_users_names,inactive_users_names=inactive_users_names,active_users_data=active_users_data,inactive_users_data=inactive_users_details,absent_users_data=absent_users_details,outside_working_no=outside_working_no,outside_working_names=outside_working_names,projects_no=projects_no,present_users=present_users,projects=projects)

@bp.route('/change_password',methods=['get'])
def change_pwd():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    #print(adminID)
    return render_template('admin_change_pwd.html',empID=adminID)


@bp.route('/cal_working_hour',methods=['get'])
def cal_working_hour():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    # Get current time as a datetime object
    data = getTotalWorkingAndBreakHrs()
    #print(data)
    return jsonify(data)
    
    
@bp.route('/profile',methods=['get','post'])
def profile():
    adminID = session.get("admin_id")
    success=None
    if(adminID == None):
        return redirect('/auth/login')
    data=getAdminDetails(adminID)
    if(request.method == 'POST'):
        req = request.form
        updateAdminDetails(adminID,req)
        data=getAdminDetails(adminID)
        success = "Profile Updated"
    return render_template('admin_profile.html',data=data,empID=adminID,success_message=success)