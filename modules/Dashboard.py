from modules.Config_db import *
import pymongo
from bson.json_util import dumps,loads
from flask import render_template,session
from bson.objectid import ObjectId
from datetime import datetime,timedelta,date
import requests
import ipaddress
import socket

#get an employees all attendance for the day
def getSingleEmployeeAttendance(empID):
    emp = db.Employees.find_one({
        "_id" : ObjectId(empID)
    })
    name = emp["first_name"]
    mail = emp["email"]
    if(name == None):
        return render_template('login.html')
    my_todays_att = db.Attendance.find( {
    "date" : datetime.fromisoformat(date.today().isoformat()),
    "employeeID" : ObjectId(empID)
    }).sort('checkInTime', pymongo.DESCENDING) 
    if(my_todays_att != None):
        json = []
        json_data = loads(dumps(list(my_todays_att)))
        for i in json_data:
            res = {
            "id" : str(i["_id"]),"name" : name,"email":mail, "in" : i["checkInTime"].strftime("%H:%M:%S"), "ip_range":i["inIpRange"] ,"breakTime": i["breakTime"]+" mins",
            "out": None, "totalhr" : None, 'is_first_checkin': i["is_first_checkin"]
            }
            if(i["checkOutTime"] != None):
                res["out"] = i["checkOutTime"].strftime("%H:%M:%S")
                res["totalhr"] = i["totalWorkingHours"]
            #print(res['is_first_checkin'])
            json.append(res)
    return json

#gets all employee details except the given employee id
def getAllEmployeesAttendance():
    data = db.Attendance.find( {
        "date" : datetime.fromisoformat(date.today().isoformat()),
        "employeeID": { "$ne": ObjectId(session.get("employee_id")) }
        }).sort('checkInTime', pymongo.DESCENDING)
    #print(data,"data")
    if(data != None):
        json = []
        json_data = loads(dumps(list(data)))
        for i in json_data:
            #print("I",i)
            emp = db.Employees.find_one({
            "_id" : ObjectId(i["employeeID"])
            }) 
            #print(i)
            if( i["checkInTime"] != None):
                inTime = i["checkInTime"].strftime("%H:%M:%S")
            else:
                inTime = None
            res = {
            "id" : str(i["_id"]),"name" : emp["first_name"]+" " +emp["last_name"],"email": emp["email"], "in" : inTime ,
            "out": None, "ip_range":i["inIpRange"],"is_first_checkin": i["is_first_checkin"]
            }
            if(i["checkOutTime"] != None):
                res["out"] = i["checkOutTime"].strftime("%H:%M:%S")
            json.append(res)
    return json 

#inserts employee checkin status time in attendance
def insertEmployeeCheckin(empID,inoffice):
    my_todays_att = db.Attendance.find( {
        "date" : datetime.fromisoformat(date.today().isoformat()),
        "employeeID" : ObjectId(empID)
        }).sort('checkOutTime', pymongo.DESCENDING)
    last_checkout = list(my_todays_att)
    breaktime = 0
    is_first_checkin = True
    
    if(len(last_checkout)!=0 and len(str(last_checkout[0]['checkOutTime']))!=0):
        diff =  datetime.now() - (last_checkout[0]['checkOutTime'])
        breaktime = round(diff.total_seconds() / 60)
        is_first_checkin = False
        
    emp_att = db.Attendance.insert_one({
        "employeeID" : ObjectId(empID),
        "date": datetime.fromisoformat(date.today().isoformat()),
        "inIpRange": inoffice,
        "checkInTime" : datetime.now(), 
        "checkOutTime" : None, #initially none 
        "breakTime" : str(breaktime),
        "totalWorkingHours":None,#initially none
        "is_first_checkin" :is_first_checkin
    })
    att = db.Attendance.find_one({
        "_id" : emp_att.inserted_id
    })
    emp = db.Employees.find_one({
        "_id" : ObjectId(empID)
    })
    res = {
        "id" : str(att["_id"]),"name" : emp["first_name"],"email":emp["email"], "in" : att["checkInTime"].strftime("%H:%M:%S"), "breakTime" : str(breaktime)+" mins",
        "in_ip_range" : att["inIpRange"], "is_first_checkin": att["is_first_checkin"]
    }
    return res

def updateEmployeeCheckout(attendance_id,empID):
    emp_att = db.Attendance.update_one(
        {'_id' : ObjectId(attendance_id)},{
        "$set":{ #pytz.timezone('Asia/Calcutta').localize(datetime.utcnow()),
        "checkOutTime" : datetime.now(),
    }})
    att = db.Attendance.find_one({
        "_id" : ObjectId(attendance_id)
    })
    inT=att["checkInTime"].strftime("%H:%M:%S")
    outT=att["checkOutTime"].strftime("%H:%M:%S")
    (h, m, s) = inT.split(':')
    t1 = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    (h, m, s) = outT.split(':')
    t2 = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    totalhr = str(t2-t1)
    emp_att = db.Attendance.update_one(
        {'_id' : ObjectId(attendance_id)},{
        "$set":{ #pytz.timezone('Asia/Calcutta').localize(datetime.utcnow()),
        "totalWorkingHours" : totalhr,
    }})
    emp = db.Employees.find_one({
        "_id" : ObjectId(empID)
    })
    res = {
        "id" : str(att["_id"]),"name" : emp["first_name"],"email":emp["email"], "in" : inT ,
        "out" : outT, "totalhr" : totalhr, "breakTime": att["breakTime"]+" mins"
    }
    return res


def getRandomQuote():
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "en",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Ensure the content type is JSON
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return "Error fetching quote: Unexpected content type: {content_type}"

        data = response.json()
        return f"{data.get('quoteText', 'Unknown quote')} —{data.get('quoteAuthor', 'Unknown author')}"
    except requests.exceptions.RequestException as e:
        return "Arise, awake, and stop not till the goal is reached.  — Swami Vivekanand"


def getProjectsByEmp(empID):
    proj = db.Projects.find({
    })
    proj_list = list(proj)
    proj_json =[] 
    emp_ = list(db.Employees.find({
        "_id": ObjectId(empID)
    }))
    #print(emp_)
    emp=emp_[0]
    for i in proj_list:
        #(i)
        if((emp.get('first_name')+' '+emp.get('last_name')) in str(i["contributors"])):
            proj_json.append({"id": str(i["_id"]),"name": i["name"]})
    return proj_json

def getHeaderInfo(emp_name):
    dt = datetime.now()
    day = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][dt.weekday()]
    if dt.hour < 12:
        greeting = 'Good Morning,'
    elif 12 <= dt.hour < 18:
        greeting = 'Good Afternoon,'
    else:
        greeting = 'Good Evening,'
    header_info = {"name" : emp_name,"day":day,"date":dt.date(), "greeting" : greeting}
    return header_info


    
