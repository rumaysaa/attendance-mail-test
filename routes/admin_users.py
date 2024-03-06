
from flask import Blueprint,render_template,session,redirect,request,url_for,jsonify
from modules.Admin_users import *
from modules.Admin_frs import *


bp = Blueprint('adm_user',__name__,)

@bp.route('/register',methods=['get','post'])
def register_user_get():
    #print(request.form.get('user_id'),"12")
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    success_message = None
    user_id = request.args.get("id")
    user = getUserById(user_id)
    #print(request.form)
    if( request.method=='POST' and str(request.form.get('userID')) == 'None'):
        req = request.form
        new_user = registerUser(req)
        #(new_user)
        if(new_user == True):
            success_message = "New user created succesfully"
            return redirect(url_for('.view_user'))
    if(request.method=='POST' and str(request.form.get('userID')) != 'None'  ):
        req = request.form
        update = updateUserById(req['userID'],req)
        #print(update)
        return redirect(url_for('.view_user'))
    return render_template('register_user.html',success_message=success_message,user_id=user_id,user=user)


@bp.route('/view',methods=['get'])
def view_user():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    users = get_users()
    return render_template('view_users.html',users=users)

@bp.route('/delete',methods=['get','delete'])
def delete_user():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    userID = request.args.get('id')
    #it will delete user as well as their credentials
    delete_status = deleteUserById(userID)
    if(delete_status != None):
        return redirect('/admin/users/view')
    else:
        return "Something went wrong"
    
@bp.route('/register_face_enc',methods=['post'])
def register_face_enc():
    userID = request.json['userid']
    #print(request.json)
    status = enroll_faces(userID)
    return {"status": status}



@bp.route('/save_video', methods=['POST'])
def upload_video():
    video = request.files['video']
    userID = session.get('userID')
    path = './static/video/'+userID+'.webm'
    video.save(path)
    save_all_frames(userID)
    os.remove(path)
    #print(x,len(x))
    return "video saved successfully"

@bp.route('/save_userID', methods=['POST'])
def save_user():
    session['userID'] = request.json['userid']
    #print(request.json['userid'])
    return "true"

@bp.route('/getUsernames')
def usernames():
    usernames = getUsernames()
    #print(usernames)
    return jsonify({"usernames":usernames})