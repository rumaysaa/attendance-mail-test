from modules.Config_db import *
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import smtplib

EMAIL_ADDRESS = "workspace.algobrainai@gmail.com"
PASSWORD = "pqjk madq dajr dcog"

#get all leaves and populatee it with Employee collection

def getLeaves(month, year):
    # Construct datetime objects for the start and end of the month
    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month+1, 1) if month < 12 else datetime(year+1, 1, 1)

    # Define the match stage to filter documents within the given month and year
    match_stage = {
        "$match": {
            "AppliedOn": {"$gte": start_of_month, "$lt": end_of_month}
        }
    }

    # Perform the aggregation
    pipeline = [
        match_stage,
        {
            "$lookup": {
                "from": "Employees",
                "localField": "employeeID",
                "foreignField": "_id",
                "as": "employee"
            }
        },
        {
            "$unwind": "$employee"
        },
        {
            "$project": {
                "emp_email": "$employee.email",
                "emp_name": {"$concat": ["$employee.first_name", " ", "$employee.last_name"]},
                "emp_avatarID": "$employee.avatarID",
                "_id": "$_id",
                "leave_type": "$leaveType",
                "start_date": "$startDate",
                "end_date": "$endDate",
                "start_hr":"$startHour",
                "end_hr":"$endHour",
                "reason": "$reason",
                "applied_on": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M:%S",
                        "date": {"$toDate": "$AppliedOn"}
                    }
                },
                "status": "$status",
                "message" : "$message"
            }
        },
        {
            "$sort": {"applied_on": -1}
        }
    ]

    # Execute the aggregation
    result = list(db.Leave.aggregate(pipeline))
    print(result)
    return result


#updates the leave status- "1" = approved ; "0" = declined
def updateLeaveStatus(leaveID,status,emp_email,app_date,msg):
    updateLeave = db.Leave.update_one(
         {'_id' : ObjectId(leaveID)},
        {
        "$set":{ 
           "status" : int(status),
           "message" : msg
        }
        }
    )
    sendLeaveStatusEmail(status,emp_email,app_date)
    return updateLeave

#Sends mail to user regarding the accepted or declined leave
def sendLeaveStatusEmail(status,emp_email,app_date):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_ADDRESS,PASSWORD)
    if(status == 1):
        msg = f"Your leave request, which was submitted on {app_date}, has been approved.  \n\n\n" \
        + f"for more details visit\n"\
        +f"https://workspace.algobrainai.com/"
    elif(status==0):
        msg = f"Your leave request, which was submitted on {app_date}, has been rejected.  \n\n\n" \
        + f"for more details visit\n"\
        +f"https://workspace.algobrainai.com/"
    email_message = f"Subject: Leave Request Status\n\n{msg}"
    s.sendmail('&&&&&&&&&&&',emp_email,email_message)
    return
