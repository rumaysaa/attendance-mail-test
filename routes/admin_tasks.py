from flask import Blueprint,render_template,session,redirect,jsonify,request
from modules.Admin_tasks import *
bp = Blueprint('adm_tasks',__name__,)
from datetime import timedelta,datetime

@bp.route('/',methods=['get'])
def tasks():
    #tasks = getTodaysTasks()
    #print(tasks)
    date = request.args.get('date')
    if date==None:
        date = datetime.now().strftime("%Y-%m-%d")
    tasks = getTasksByDate(date)
    return render_template('admin_tasks.html',tasks=tasks)