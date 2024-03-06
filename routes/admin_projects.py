
from flask import Blueprint,render_template,session,redirect,request
from modules.Admin_projects import *

bp = Blueprint('adm_projs',__name__,)

@bp.route('/create',methods=['get','post'])
def create_project():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    proj_details = None
    projectID = request.args.get('id')
    if( projectID != None):
        proj_details = getProjectDetailsById(request.args.get('id'))
    if(request.form.get("projectId")!= 'None' and request.method =='POST'):
        status = updateProjectById(request.form.get("projectId"),request.form)
        if(status != None):
            return redirect('/admin/projects/view')
        else:
            return "Something went wrong while updation"
    emp_details =  getEmployeesNameAndDesig()
    interns=[]
    employees=[]
    hrs=[]
    managers=[]
    others=[]
    for i in emp_details:
        if(i['desig'] == 'Intern'):
            interns.append(i['name'])
        if(i['desig'] == 'Employee'):
            employees.append(i['name'])
        if(i['desig'] == 'Manager'):
            managers.append(i['name'])
        if(i['desig'] == 'HR'):
            hrs.append(i['name'])
        if(i['desig'] == 'Other'):
            others.append(i['name'])
    success_msg=None
    if(request.method=='POST' and request.form.get('projectId') == 'None'):
        proj = createProject(request.form)
        if(proj != True):
            return proj
        success_msg = "Project created successfully"
        return redirect('/admin/projects/view')
    return render_template('create_project.html',success_msg=success_msg,interns=interns,employees=employees,hrs=hrs,managers=managers,others=others,proj_details=proj_details,projectID=projectID)


@bp.route('/view',methods=['get'])
def view_project():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    proj = getProjects()
    #print(proj)
    return render_template('view_project.html',proj=proj)

@bp.route('/delete',methods=['get','delete'])
def delete_project():
    adminID = session.get("admin_id")
    if(adminID == None):
        return redirect('/auth/login')
    projectID = request.args.get('id')
    delete_status = deleteProjectById(projectID)
    if(delete_status != None):
        return redirect('/admin/projects/view')
    else:
        return "Something went wrong"