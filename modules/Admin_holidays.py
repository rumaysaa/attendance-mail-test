
from modules.Config_db import *
import pymongo
from bson.json_util import dumps,loads
from flask import session
from bson.objectid import ObjectId
from datetime import date,datetime,timedelta

#get Holidays by id 
def getHolidayById(id):
    holiday = db.Holidays.find_one({
        "_id": ObjectId(id)
    })
    data = {
        "id": str(holiday['_id']),
        "name": holiday['name'],
        "date" : str(datetime.strptime(str(holiday['date']), '%Y-%m-%d %H:%M:%S').date()),
        "instruction1" : holiday['instruction1'],
        "instruction2" : holiday['instruction2'],
        "instruction3" : holiday['instruction3']
        
    }
    return data

#updateHolidayById
def updateHolidayById(id,req):
    holiday = db.Holidays.update_one(
        {'_id' : ObjectId(id)},
        {
        "$set":{ 
            "name" : req["name"],
            "date" : datetime.fromisoformat(req["date"]),
            "instruction1": req["instruction1"],
            "instruction2": req["instruction2"],
            "instruction3": req["instruction3"]
        }
        })
    print(holiday)
    return holiday
    
    
#inserts Holiday record
def create_holiday(req):
    holi = db.Holidays.insert_one({
        "name" : req['name'],
        "date" : datetime.fromisoformat(req['date']) ,
        "instruction1" : req['instruction1'],
        "instruction2" : req['instruction2'],
        "instruction3" : req['instruction3']
    })
    return holi

#get upcoming holidays
def getHolidayDetails():
    data = list(db.Holidays.find({
        "date": { "$gte": datetime.fromisoformat( date.today().isoformat())}
    }).sort('date', 1))
    #print(data,date.fromisoformat( date.today().isoformat()))
    dd=None
    month=None
    json=[]
    for i in data:
        date_ = str(datetime.strptime(str(i['date']), '%Y-%m-%d %H:%M:%S').date())
        dd = date_.split('-')[2]
        month = getMonth(date_.split('-')[1])
        json.append({
            "id" : i["_id"],
            "name":i['name'],
            "ins1" : i['instruction1'],
            "ins2" : i['instruction2'],
            "ins3" :i['instruction3'],
            "day":dd,
            "month":month
        })
        #print(date_)
    return json

#getting month name from number
def getMonth(index):
    return [
        'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
    ][int(index)-1]
    

def deleteHolidayById(id):
    try:
        db.Holidays.delete_one(
            {"_id": ObjectId(id)}
        )
    except:
        return False
    finally:
        return True