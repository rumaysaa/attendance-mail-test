
import pymongo
from modules.Config_db import *
from datetime import datetime,date,timedelta
from bson.objectid import ObjectId

#creates Notification record
def createNotification(data):
    #print(data)
    noti = db.Notifications.insert_one({
        "subject":data['subject'],
        "notification" : data['content'],
        "dateTime" : datetime.now(),
        "readBy": []
        })
    noti = str(noti.inserted_id)
    return noti

#get all notifications from Notifications collection sorted by date in descending order 
def getNotificationDetails():
    data = db.Notifications.find({}).sort('dateTime', -1)
    formated_data = None
    if(data != None):
        formated_data=[]
        for i in data:
            dateTime =  i['dateTime'].strftime('%A, %d. %B %Y %I:%M%p')
            # convert string to datetime
            dt1 = datetime.strptime(str(i['dateTime']), "%Y-%m-%d %H:%M:%S.%f")
            dt2 = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            # difference between datetime in timedelta
            #print((dt2.date()-dt1.date())==)
            delta = dt2.date()-dt1.date()
            #print(f'Difference is {delta.days} days')
            if(delta == timedelta(days=0)):
                dateTime = "Today "+ i['dateTime'].strftime("%H:%M")
            elif(delta == timedelta(days=1)):
                dateTime = "Yesterday "+ i['dateTime'].strftime("%H:%M")
            employee_names = []
            for empId in i['readBy']:
                emp= db.Employees.find_one({
                    "_id": ObjectId(empId)
                })
                employee_names.append(emp['first_name']+' '+emp['last_name'])
            formated_data.append({
                "id" : i['_id'],
                "subject":i['subject'],
                "notification" :i['notification'],
                "dateTime" : dateTime,
                "readBy" : employee_names,
                "readById": i['readBy']
            })
    return formated_data

#update the notification collection "read_by" list and iinserts the read employee's empid
def markEmpAsRead(empID,notiID):
    noti = list(db.Notifications.find({
        "_id": ObjectId(notiID)
    }))[0]
    #print(noti)
    if(len(noti) != 0):
        sub = noti['subject']
        notification= noti['notification']
        dateTime= noti['dateTime']
        readBy = noti['readBy']
        if(empID in readBy):
            return "already Read"
        readBy.append(empID)
        updated_noti = {
        "subject" :sub,
        "notification" :notification,
        "dateTime":dateTime,
        "readBy" : readBy
        }
        update = db.Notifications.update_one(
        {'_id' : ObjectId(notiID)},
        {
        "$set": updated_noti
        }
        )
        #print(updated_noti,update)
    return "read"

#shows unread notifications number
def count_read_noti(empID):
    count = 0
    notifications = list(db.Notifications.find({
    }))
    for noti in notifications:
        if(empID not in noti['readBy']):
            count+=1
    return count;

def deleteNotificationById(id):
    try:
        db.Notifications.delete_one(
            {"_id": ObjectId(id)}
        )
    except:
        return False
    finally:
        return True