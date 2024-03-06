from modules.Config_db import *
from datetime import datetime

#get tasks at the given date fro tasks collection, populate  Employees collection and Projects to concate more details 
def getTasksByDate(date):
    # Convert the selected date string to a datetime object
    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    # Construct pipeline with date filter
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": datetime.combine(target_date, datetime.min.time()),
                    "$lt": datetime.combine(target_date, datetime.max.time())
                }
            }
        },
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
            "$lookup": {
                "from": "Projects",
                "localField": "projectID",
                "foreignField": "_id",
                "as": "project"
            }
        },
        {
            "$unwind": "$project"
        },
        {
            "$project": {
                "emp_email": "$employee.email",
                "emp_name": {"$concat": ["$employee.first_name", " ", "$employee.last_name"]},
                "emp_avatarID": "$employee.avatarID",
                "project_name": "$project.name",
                "project_leader": "$project.leader",
                "task_type": "$task_type",
                "task_detail": "$task_detail",
                "time": {
                    "$dateToString": {
                        "format": "%H:%M",
                        "date": {"$toDate": "$date"}
                    }
                },
                "status": "$status"
            }
        },
        {
            "$sort": {"applied_on": -1}
        }
    ]
    result = list(db.Tasks.aggregate(pipeline))
    return result