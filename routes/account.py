
from flask import Blueprint,render_template,session,redirect,request, url_for
from datetime import datetime
bp = Blueprint('acc',__name__,)
from modules.Admin_noti import *
from modules.Account import *
from modules.Auth import getCredentialByEmployeeID, verifyPass
from modules.Dashboard import getHeaderInfo
from modules.Admin_holidays import getHolidayDetails
from modules.Admin_events import getEventDetails

@bp.route('/',methods=['get','post'])
def account():
    empID = session.get("employee_id")
    if(empID == None): 
        return redirect('/auth/login')
    account_details = getAccountDetails(empID)
    change_success=None
    null_err=None
    avatar_id = request.args.get('id')
    if(avatar_id != None):
        #print(avatar_id)
        response = updateAccountAvatar(empID,avatar_id)
        #print(response)
        return redirect(url_for('.account'))
    header_info = getHeaderInfo(account_details['fname'])
    no_noti = count_read_noti(empID)
    no_holi = len( getHolidayDetails())
    no_event = len(getEventDetails())
    return render_template('index.html', header_info=header_info,page='account.html', acc_data=account_details,change_success=change_success,empID=empID,null_err=null_err,no_noti=no_noti,no_holi=no_holi,no_event=no_event)

@bp.route('/update_pwd',methods=['post'])
def update_acc():
    empID = request.json.get("empID")
    #print(request.json)
    unmatched_err=None
    oldpwd_err=None
    change_success=None
    if(request.json.get("old_pwd") != None):
        pass_details = request.json
        org_pass = getCredentialByEmployeeID(empID)
        #print(pass_details,pass_details["old_pwd"],org_pass)
        check_oldpwd = verifyPass(pass_details["old_pwd"],org_pass["password"])
        if(pass_details['new_pwd1'] != pass_details['new_pwd2']):
            unmatched_err = True
        if(check_oldpwd == False):
            oldpwd_err = True
        elif(check_oldpwd == True and pass_details['new_pwd1'] == pass_details['new_pwd2']):
            updatePasswordByEmpId(empID,pass_details['new_pwd1'])
            change_success = True
    return {"unmatched_err" :unmatched_err,"oldpwd_err":oldpwd_err,"change_success":change_success}


@bp.route('/redirect_loader', methods=['get'])
def redirect_loader():
    return render_template("redirect.html")

@bp.route('/profile',methods=['post'])
def set_profile():
    return request.form

@bp.route('/set_reminder',methods=['post'])
def set_reminder():
    print(request.json)
    updateReminder(request.json)
    return {"status":"updating"}