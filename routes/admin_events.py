
from flask import Blueprint,render_template,session,jsonify,request, url_for,redirect

bp = Blueprint('adm_events',__name__,)

from modules.Admin_events import *


@bp.route('/',methods=['get'])
def create_events():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    return render_template('admin_events.html')

@bp.route('/create',methods=['post'])
def create_events_post():
    data = createEvent(request.form)
    return render_template('admin_create_events.html')

@bp.route('/get_json',methods=['get'])
def get_json():
    return getEventDetails()