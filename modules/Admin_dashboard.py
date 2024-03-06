
from modules.Config_db import *
import pymongo
from bson.json_util import dumps,loads
from flask import session
from bson.objectid import ObjectId
from datetime import datetime,date
                

#finds current date's records from Attendance Collection whose checkout is None = active
def getActiveEmployees():
    data = db.Attendance.find( {
        "date" : datetime.fromisoformat(date.today().isoformat()),
        "checkOutTime" : None
        }).sort('checkInTime', pymongo.DESCENDING)
    json = []
    if(data != None):
        json_data = loads(dumps(list(data)))
        for i in json_data:
            emp = db.Employees.find_one({
            "_id" : ObjectId(i["employeeID"])
            }) 
            if( i["checkInTime"] != None):
                inTime = i["checkInTime"].strftime("%H:%M:%S")
            else:
                inTime = None
            res = {
            "id" : str(i["_id"]),"employeeID":str(i['employeeID']),"name" : emp["first_name"]+" " +emp["last_name"],"email": emp["email"], "in" : inTime ,
            "breakTime": i["breakTime"]+" mins","status":i["inIpRange"]
            }
            if(i["checkOutTime"] != None):
                res["out"] = i["checkOutTime"].strftime("%H:%M:%S")
            json.append(res)
    return json 


#gets inactive employeeIDs from substracting 2 sets od total employees and active employees
def getInactiveEmployees(total_emps,active_emps):
    total_emps_ids = set()
    active_emps_ids = set()
    for i in total_emps:
        _id = str(i['_id'])
        total_emps_ids.add(_id)
    for i in active_emps:
        ac_id = str(i['employeeID'])
        active_emps_ids.add(ac_id)
    return total_emps_ids-active_emps_ids

#get absent employees
def getAbsentEmployees(total_emps,present_emps):
    total_emps_ids = set()
    present_emps_ids = set()
    for i in total_emps:
        _id = str(i['_id'])
        total_emps_ids.add(_id)
    for i in present_emps:
        ac_id = str(i['employeeID'])
        present_emps_ids.add(ac_id)
    return total_emps_ids-present_emps_ids

#finds current date's checked out attendance
def get_todays_checked_out_att():
    data = db.Attendance.find({
    "date" : datetime.fromisoformat(date.today().isoformat()),
    "checkOutTime": { "$ne": None}
    })
    return data

#gets all the records from Project collection
def getProjects():
    data = db.Projects.find({})
    return list(data)

#finds all attendance records of today's date
def getPresentEmployees():
    data = list(db.Attendance.find({
    "date" : datetime.fromisoformat(date.today().isoformat()),
    }))
    employee_data = []
    if(data != None):
        for i in data:
            emp = db.Employees.find_one({
            "_id" : ObjectId(i["employeeID"])
            }) 
            res = {
            "employeeID": str(emp["_id"]) ,"name" : emp["first_name"]+" " +emp["last_name"],"email": emp["email"], "in" : i["checkInTime"].strftime("%H:%M:%S") ,
            "breakTime": i["breakTime"]+" mins","status":i["inIpRange"]
            }
            if(i["checkOutTime"] != None):
                res["out"] = i["checkOutTime"].strftime("%H:%M:%S")
            employee_data.append(res)
    return employee_data

#finds Admin record in Employees collection and updates the email and phone
def updateAdminDetails(Adm_id,req):
    adm = db.Employees.update_one(
        {'_id' : ObjectId(Adm_id)},
        {
        "$set":{ 
            "email" : req["email"],
            "phone" : req["phone"]
        }
        })
    return adm

#finds Admin details from employees
def getAdminDetails(admID):
    data = db.Employees.find_one({
        "_id" : ObjectId(admID)
    })
    json = {"email" : data["email"],
            "phone" : data["phone"]
            }
    return json

#aggregates current days attendance record by EmployeeID and sums up total hours and total break hours
def getTotalWorkingAndBreakHrs():
    pipeline = [
            {
        '$match': {
            'date': datetime.fromisoformat(date.today().isoformat())
        }
    },
       { '$addFields': {
            'checkOutTime': {
                '$cond': {
                    'if': {'$eq': ['$checkOutTime', None]},  # Check if checkOutTime is null
                    'then': datetime.now(),  # Set current time as checkOutTime
                    'else': '$checkOutTime'  # Use existing checkOutTime
                }
            },
            'breakTimeHours': {  # Convert break time to hours
                '$divide': [
                    {'$toInt': '$breakTime'},  # Convert break time string to integer
                    60  # Convert minutes to hours
                ]
            }
        }
    },
    {
        '$addFields': {
            'timeDifference': {
                '$divide': [
                    {'$subtract': ['$checkOutTime', '$checkInTime']},  # Calculate time difference in milliseconds
                    3600000  # Convert milliseconds to hours
                ]
            }
        }
    },
    {
        '$group': {
            '_id': '$employeeID',                   # Group by employee_id
            'total_hours': {'$sum': '$timeDifference'},  # Sum the total working hours
            'total_breaktime': {'$sum': '$breakTimeHours'}
        }
    }
]
    #perform aggregation
    result = list(db.Attendance.aggregate(pipeline))
    #print(result)
    data=[]
    for i in result:
        emp = db.Employees.find_one({
            "_id" : ObjectId(i["_id"])
        })
        data.append({"name":emp['first_name']+" "+emp['last_name'],"working_hrs":i['total_hours'],"break_hrs":i["total_breaktime"]})
    return data