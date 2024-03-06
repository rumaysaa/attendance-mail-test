from flask import Blueprint,render_template,url_for,redirect,request

from modules.Admin_holidays import *

bp = Blueprint('adm_holidays',__name__,)


@bp.route('/',methods=['get'])
def view_holidays():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    holidays = getHolidayDetails()
    return render_template('admin_holidays.html',holidays=holidays)

@bp.route('/create',methods=['get'])
def view_create_holidays():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    holi_id = request.args.get("id")
    holiday= None
    if(holi_id != None):
        holiday = getHolidayById(holi_id)
    return render_template('admin_create_holidays.html',data = holiday)

@bp.route('/create',methods=['post'])
def create_holidays():
    id = request.form.get("holiday_id")
    if(id != ''):
        updated = updateHolidayById(id,request.form)
    else:
        created = create_holiday(request.form)
        print("create")
    return redirect(url_for('.view_holidays'))

@bp.route('/delete',methods=['get'])
def delete_holidays():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    id = request.args.get("id")
    deleted = deleteHolidayById(id)
    #print(deleted)
    return redirect('/admin/holidays')