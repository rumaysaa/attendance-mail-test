from modules.Config_db import *
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps


#create project record
def createProject(req):
    contri = []
    for i in req:
        if i[:6]=='contri':
            contri.append(req[i])
    #print(contri)
    proj = db.Projects.insert_one({
        "name" : req["projectName"],
        "start_date" : datetime.fromisoformat(req["startDate"]),
        "end_date" : datetime.fromisoformat(req["endDate"]),
        "project_type" : req['projectType'],
        "client_name" : req.get("clientName"),
        "company_name" : req.get("clientCompanyName"),
        "contributors" : contri,
        "assigned_by" : req["assignedBy"],
        "leader" : req["leader"]
        }) 
    projID = str(proj.inserted_id)
    if(projID == None):
        return "something went wrong"
    else:
        return True

#returns name and designations of all employees
def getEmployeesNameAndDesig():
    emps = db.Employees.find({})
    data = []
    for i in list(emps):
        data.append({
            "name" : i['first_name']+" "+i['last_name'],
            "desig" : i["designation"]
        })
    return data

#returns all projects
def getProjects():
    projects =  list(db.Projects.find({}))
    data = []
    for project in projects:
        data.append({
            "id" : project['_id'],
            "name": project['name'],
            "st_date": str(project['start_date'].day) +'/'+ str(project['start_date'].month)+'/'+str(project['start_date'].year),
            "en_date":str(project['end_date'].day) +'/'+ str(project['end_date'].month)+'/'+str(project['end_date'].year),
            "contri": ', '.join(project['contributors']),
            "assigned_by" : project['assigned_by'],
            "leader": project['leader']
        })
    return data

#finds a record from Project using projectId
def getProjectDetailsById(projectId):
    proj = list(db.Projects.find({
        "_id" : ObjectId(projectId)
    }))
    data=None
    if(len(proj)!= 0):
        proj = proj[0]
        data = {
            "id" : str(proj['_id']), 
            "name" : proj['name'],
            "start_dt" : proj['start_date'].date().isoformat(),
            "end_dt" : proj['end_date'].date().isoformat(),
            "contri": proj['contributors'],
            "proj_type": proj['project_type'],
            "assigned_by": proj['assigned_by'],
            "leader": proj['leader']
            }
    return data

#updates project using project id
def updateProjectById(proj_id,req):
    contri = []
    for i in req:
        if i[:6]=='contri':
            contri.append(req[i])
    try:
        project = db.Projects.update_one(
            {"_id" : ObjectId(proj_id) },
            {"$set":{ 
            "name" : req['projectName'],
            "start_date" : datetime.fromisoformat(req["startDate"]),
            "end_date" : datetime.fromisoformat(req["endDate"]),
            "contributors": contri,
            "project_type": req['projectType'],
            "assigned_by": req['assignedBy'],
            "leader": req['leader']
            }}
            )
    except:
        return None
    return "Success"

#delete project by project id
def deleteProjectById(proj_id):
    try:
        db.Projects.delete_one(
            {"_id": ObjectId(proj_id)}
        )
    except:
        return None
    return "Success"