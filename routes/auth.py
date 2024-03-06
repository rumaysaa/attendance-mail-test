from flask import Blueprint,render_template,session,redirect,url_for,request,jsonify

bp = Blueprint('auth',__name__,)

from modules.Auth import *
from modules.Account import updatePasswordByEmpId

@bp.route('/login', methods=['get'])
def login():
    return render_template('login.html')

@bp.route('/logout')
def logout():
    if(session.get("employee_id")!=None):
        session.pop("employee_id", None)
        session.pop("current_att_id", None)
        session.pop("indiv_att", None)
    if(session.get("admin_id") != None):
        session.pop("admin_id", None)
    return redirect(url_for('.login'))

@bp.route('/login',methods=['post'])
def checkCredentials():
    username = request.form["username"]
    pwd =  request.form["password"]
    cred = getCredentialByUsername(username)
    if(cred == None):
            return render_template('login.html', uname_err = "Invalid Username!")
    if(not verifyPass(pwd, cred["password"])):
        return render_template('login.html', uname = username,pass_err = "Invalid Password!")
    if(username=='Admin' and verifyPass(pwd, cred["password"])):
        session["admin_id"] = str(cred["employeeID"])
        return redirect(url_for('adm_dash.admin'))
    session["employee_id"] = str(cred["employeeID"])
    return redirect(url_for('dash.index'))

@bp.route('/otp_verification',methods=['get'])
def otp_verification():
    verified= False
    if((session.get('employee_id_from_email') and session.get('otp')) != None):
        verified = True
    return render_template('otp_veri.html',verified=verified)

@bp.route('/reset_password',methods=['get','post'])
def reset_password():
    #print(session.get('employee_id_from_email'))
    if(session.get('employee_id_from_email')==None):
        return redirect('/auth/otp_verification')
    if(request.method == 'POST'):
        #print(request.form)
        updatePasswordByEmpId(session['employee_id_from_email'],request.form.get('conf_new_pwd'))
        return render_template("redirect.html")
    return render_template('reset_pwd.html')

@bp.route('/otp_verification/check_email',methods=['post'])
def checkEmail():
    #print(request.json)
    response = verifyEmail(request.json['email'])
    if(response==None):
        return jsonify({"error":"Email not found"})
    mail = response.get("email")
    session.pop('otp',None)
    session.pop('employee_id_from_email',None)
    if(mail!=None):
        s,msg,OTP = set_OTP()
        email_message = f"Subject: OTP for Password Reset\n\n{msg}"
        s.sendmail('&&&&&&&&&&&',mail,email_message)
        session['otp'] = OTP
        session['employee_id_from_email'] = str(response["_id"])
        return jsonify({"email": mail})
    


@bp.route('/otp_verification/check_otp',methods=['post'])
def check_otp():
    isValid= False
    #print(request.json)
    if(str(session['otp']) == str(request.json['otp'])):
        isValid = True
    return {"isValid": isValid}
