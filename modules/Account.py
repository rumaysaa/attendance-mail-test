from modules.Config_db import *
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
import threading
import schedule,time
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#finds record using given id and updates it
def updateAccountDetails(req):
    emp_att = db.Employees.update_one(
        {'_id' : ObjectId(req["emp_id"])},
        {
        "$set":{ 
            "first_name" : req["fname"],
            "last_name" : req["lname"],
            "email": req["mail"],
            "phone": req["phone"],
            "dob": req["dob"],
            "joining_date": req["joining_date"]
            #"last_edited" : datetime.now()
        }
        })
    return emp_att

#finds a record using ID and returns it
def getAccountDetails(empID):
    data = db.Employees.find_one({
        "_id" : ObjectId(empID)
    })
    json = {"fname" : data["first_name"],
            "lname" : data["last_name"],
            "email" : data["email"],
            "phone" : data["phone"],
            "dob" : data["dob"], 
            "joining_date":data["joining_date"],
            "gender": data["gender"],
            "desig" : data['designation'],
            "shift" : data['shift'],
            "address": data['address'],
            "city": data['city'],
            "avatarID" : data['avatarID'],
            "reminders" : data.get('reminders')
            }
    if json['reminders'] == None:
        json['reminders'] = []
    return json

#finds credential using given employeeID and updates it by new password
def updatePasswordByEmpId(empID,new_pass):
    update_pwd = db.Credentials.update_one(
         {'employeeID' : ObjectId(empID)},
        {
        "$set":{"password" : sha256_crypt.hash(new_pass)}
        })
    return update_pwd

#finds a record using employee Id and updates the avatarId of that record
def updateAccountAvatar(employee_id,avatar_id):
    #print(employee_id,avatar_id)
    update_avatar = db.Employees.update_one(
         {'_id' : ObjectId(employee_id)},
        {
        "$set":{"avatarID" : avatar_id}
        })
    return update_avatar

def updateReminder(req):
    update =  db.Employees.update_one(
        {'_id' : ObjectId(req["id"])},
        {
        "$set":{ 
            "reminders" : req["days"]
        }
        })
    emp_mail = list(db.Employees.find({
        "_id": ObjectId(req["id"])
    }))[0]['email']
    print(emp_mail)
    email_scheduling_thread = threading.Thread(target=schedule_emails(emp_mail,req["days"]))
    email_scheduling_thread.start()
    return update


# Function to send email
def send_checkin_email(emp_email,days):
    if(inweekday(days)):
        EMAIL_ADDRESS = "workspace.algobrainai@gmail.com"
        PASSWORD = "pqjk madq dajr dcog"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(EMAIL_ADDRESS, PASSWORD)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Daily Reminder"
        message["From"] = EMAIL_ADDRESS
        message["To"] = emp_email
        text_part = MIMEText("Did you check-in? \nIf not, please visit the link below. \n\n https://workspace.algobrainai.com", "plain")
        message.attach(text_part)
        s.sendmail(EMAIL_ADDRESS, emp_email, message.as_string())
        print("sending mail")
        s.quit()
    return True

# Function to send email
def send_checkout_email(emp_email,days):
    if(inweekday(days)):
        EMAIL_ADDRESS = "workspace.algobrainai@gmail.com"
        PASSWORD = "pqjk madq dajr dcog"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(EMAIL_ADDRESS, PASSWORD)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Daily Reminder"
        message["From"] = EMAIL_ADDRESS
        message["To"] = emp_email
        text_part = MIMEText("Did you check-out? \nIf not, please visit the link below. \n\n https://workspace.algobrainai.com", "plain")
        message.attach(text_part)
        s.sendmail(EMAIL_ADDRESS, emp_email, message.as_string())
        print("sending mail")
        s.quit()
    return True

# Function to schedule emails
def schedule_emails(mail,days):
    # Schedule email at 9:30 AM every day (except Sundays)
    schedule.every().day.at("10:00").do(send_checkin_email,emp_email=mail,days=days)
    schedule.every().day.at("10:15").do(send_checkin_email,emp_email=mail,days=days)
    schedule.every().day.at("11:00").do(send_checkin_email,emp_email=mail,days=days)
    schedule.every().day.at("11:30").do(send_checkin_email,emp_email=mail,days=days)
    schedule.every().day.at("12:00").do(send_checkout_email,emp_email=mail,days=days)
    schedule.every().day.at("12:30").do(send_checkout_email,emp_email=mail,days=days)
    schedule.every().day.at("15:00").do(send_checkout_email,emp_email=mail,days=days)
    schedule.every().day.at("13:00").do(send_checkout_email,emp_email=mail,days=days)

    # Loop to keep the program running
    while True:
        schedule.run_pending()
        time.sleep(1)
    return "completed"

  
def inweekday(days):
    week = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    index = datetime.today().weekday()
    print(week[index] in days)
    return week[index] in days
