from modules.Config_db import *
import pymongo
from bson.json_util import dumps,loads
from flask import render_template,session
from bson.objectid import ObjectId
from datetime import datetime,timedelta,date
import requests
import smtplib
from os import environ 
EMAIL_ADDRESS = "workspace.algobrainai@gmail.com"
PASSWORD = "pqjk madq dajr dcog"

def leaveApply(data):
    leave = db.Leave.insert_one({
    "employeeID": ObjectId(data['empID']),
    "leaveType": data['leaveType'],
    "startDate": data['startDate'],
    "endDate":data["endDate"],
    "startHour": data["startHr"],
    "endHour":data["endHr"],
    "reason" :data['reason'],
    "AppliedOn": datetime.now(),
    "status": -1,# -1 =pending, 1=Accept, 0=reject,
    "message" : ""
    })
    emp = db.Employees.find_one({
        "_id": ObjectId(data["empID"])
    })
    #print(emp)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_ADDRESS, PASSWORD)
    if(data['leaveType']=="Half day"):
        msg = f"{emp['first_name']} {emp['last_name']}\n{emp['email']}\n\n" \
        + f"Leave Details: \n\nStart Date: {data['startDate']}\nStart Time: {data['startHr']}\nEnd Time: {data['endHr']}\n\n" \
        + f"{data['reason']} \n\nApplied on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        msg = f"{emp['first_name']} {emp['last_name']} \n{emp['email']}\n\n" \
        + f"Leave Details: \n\nStart Date: {data['startDate']}\nEnd Date: {data['endDate']}\n\n" \
        + f"{data['reason']} \n\nApplied on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    email_message = f"Subject: {data['leaveType']} Leave\n\n{msg}"
    s.sendmail('&&&&&&&&&&&',"rumaysa.babulkhair@gmail.com",email_message)
    return leave

def getLeaveByEmpID(empID):     
    pipeline = [
    {"$match": {"employeeID": ObjectId(empID)}},
    {"$sort": {"AppliedOn": -1}},
    {
        "$addFields": {
            "appliedOn": {
                "$dateToString": {
                    "format": "%Y-%m-%d %H:%M:%S",
                    "date": "$AppliedOn"
                }
            }
        }
    }
]
    leaves = db.Leave.aggregate(pipeline)
   #print(list(leaves))
    return list(leaves)
