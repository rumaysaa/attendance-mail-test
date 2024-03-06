from modules.Config_db import *
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64,os

EMAIL_ADDRESS = "workspace.algobrainai@gmail.com"
PASSWORD = "pqjk madq dajr dcog"

#registers user deetails in Employees collection and Credentials in Credential collectioon
def registerUser(req):
    emp = db.Employees.insert_one({
        "first_name" : req["fname"],
        "last_name" : req["lname"],
        "gender": req["gender"],
        "address": req['add'],
        "city": req['city'],
        "email" : req['email'],
        "phone" : req['phone'],
        "dob" : req["dob"],
        "joining_date" : req["joining_date"],
        "shift" : req["shift"],
        "designation" : req["desig"],
        "avatarID": "profile"
        }) 
    empID = str(emp.inserted_id)
    cred = db.Credentials.insert_one({
        "employeeID" : ObjectId(empID),
        "username": req["username"],
        "password" : sha256_crypt.hash(req["fname"].strip().lower()+"@algo123")
    })
    credID = str(cred.inserted_id)
    #send credentials to employee's email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_ADDRESS, PASSWORD)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome Onboard!"
    message["From"] = EMAIL_ADDRESS
    message["To"] = req['email']
    # Read the image file
    curr_path= str(os.getcwd())
    print(os.getcwd())
    with open("static/images/welcome.jpeg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    msg = createHtmlMail(req['fname'],req['lname'],req['username'],encoded_image)
    html_part = MIMEText(msg, "html")
    message.attach(html_part)
    # Send the email
    s.sendmail(EMAIL_ADDRESS, req['email'], message.as_string())
    # Close the connection to the SMTP server
    s.quit()
    return False
  
#get usernames from Credential collection
def getUsernames():
    creds= db.Credentials.find({})
    data=[]
    for cred in creds:
        data.append(cred['username'])   
    return data
        
#get all users except admin 
def get_users():
    users = list(db.Employees.find({
        "_id" : {"$ne": ObjectId("65d5c2bdb6fb19d2beb15375")}
        
    }))
    json = []
    for user in users:
        json.append({
            "id" : str(user['_id']),
            "name" : user['first_name']+' '+ user['last_name'],
            "email" : user["email"],
            "phone" : user["phone"],
            "joining_dt" : user["joining_date"],
            "desig": user["designation"],
            "avatar":user["avatarID"]
        })
        
    #print(json)
    return json

#delete user by user id
def deleteUserById(user_id):
    try:
        db.Employees.delete_one(
            {"_id": ObjectId(user_id)}
        )
        db.Credentials.delete_one(
            {"employeeID": ObjectId(user_id)}
        )
    except:
        return None
    return "Success"

#get all users by id
def getUserById(user_id):
    try:
        user = (db.Employees.find_one({
            "_id" : ObjectId(user_id)
        }))
        
        user_data = {
            "id" : str(user['_id']),
            "fname": user['first_name'],
            "lname" : user['last_name'],
            "dob": user['dob'],
            "joining_date": user['joining_date'],
            "gender": user["gender"],
            "desig" : user['designation'],
            "shift" : user.get('shift'),
            "add": user['address'],
            "city": user['city'],
            "email": user['email'],
            "phone": user['phone']
        }
        #print(user_data)
    except:
        return None
    return user_data

#updates user by user id
def updateUserById(userID,req):
    #print(userID)
    up_user = db.Employees.update_one(
            {"_id" : ObjectId(userID)},
            {"$set":{ 
            "first_name": req['fname'],
            "last_name" : req['lname'],
            "dob": req['dob'],
            "joining_date": req['joining_date'],
            "gender": req["gender"],
            "designation" : req['desig'],
            "shift" : req['shift'],
            "address": req['add'],
            "city": req['city'],
            "email": req['email'],
            "phone": req['phone']
            }}
            )
    #print(up_user)
    return "Success"



def createHtmlMail(fname,lname,username,encoded_image):
    html = '''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome </title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;600&display=swap');

    body,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    div {
      margin: 0;
      padding: 0;
    }

    body {
      background-color: #f4f4f4;
      /* Light mode background color */
      color: #333;
      /* Light mode text color */
      font-family: 'Outfit', sans-serif;
      line-height: 30px;
      font-size: 15px;
      font-weight: 300;
    }

    :root {
      --dark-color: black;
      --light-color: white;
    }

    .svg {
      fill: var(--dark-color);
      /* Default color for dark mode */
    }

    #bottom {
      padding: 0px auto;
      margin: 10px auto;
      font-size: 14px;
      line-height: 24px;
      font-weight: 300;
    }

    footer {
      margin-top: 0 !important;
    }

    .container {
      max-width: 751px;
      margin: 0 auto;
    }

    .header-img {
      width: 100%;
      height: auto;
      display: block;
    }

    h2 {
      font-size: 24px;
    }

    .content {
      max-width: 651px;
      margin: 15px auto 0 auto;
      line-height: 30px;
      padding: 18px;
    }

    #reason {
      padding: 1px;
      background-color: #E7FFF9;
      border-radius: 10px;
      font-weight: 400;
    }

    #reason p {
      padding: 0px 10px;
    }

    .value {
      font-weight: 600 !important;
    }

    @media (prefers-color-scheme: dark) {
      body {
        background-color: #1a1a1a;
        /* Dark mode background color */
        color: #ffffff;
        /* Dark mode text color */
      }

      hr {
        border-color: hsla(0, 0%, 100%, 0.3);
      }

      .svg {
        fill: var(--light-color);
        /* Color for light mode */
      }

      #bottom {
        font-weight: light;
        color: hsla(0, 0%, 100%, 0.3) !important;
      }

      #reason {
        background-color: #323232;
        border-radius: 10px;
      }
    }
  </style>
</head>
<body>
  <header class="container welcome">
    <img src="https://drive.google.com/uc?export=download&id=1JtPZRN3nU74Wpa3LF5-zy3UY1swi1dGM" alt="Image" style="width:100%">
  </header>
  <main class="container">
    <div class="content">
      <p> Hello '''+fname+ ' '+lname+''', </p>
      <br />
      <h2>Welcome Onboard! Get started with Workspace 🚀</h2>
      <br />

      <br />

      <p> So what’s next? You can login into your company profile using the credentials provided below. Click on this link to enter Workspace <span style="color: #0000EE"><u> https://workspace.algobrainai.com/</u></span>
      </p>
      
      <b>Username:</b>'''+ username +'''<br>
      <b>Password:</b>'''+fname.strip().lower()+'@algo123'+ '''<br>
      <br />
      <p> You must check in daily in workspace before starting your work. Workspace is an in-house attendance tracker customised to record and assign tasks for efficient working. Change your password as soon as you login for security reasons. Welcome to the Team. Happy Coding!!😊</p>
      <br>

      <p style="font-family: 'Pacifico', cursive;"
    font-size: 35px;">
        With Love,
      </p>
      <p> The Algobrain AI Team </p>
      <br />

      <hr />
      <br />
    </div>
  </main>
</body>

</html>'''
    return html
