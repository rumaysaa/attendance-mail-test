import certifi
from pymongo.mongo_client import MongoClient

from os import environ 
#uri = f"mongodb+srv://{environ.get('MONGO_UNAME')}:{environ.get('MONGO_PASS')}@cluster0.vabsxvc.mongodb.net/Attendance_management?retryWrites=true&w=majority"
#uri = "mongodb+srv://attendance_proj:vAezIHAOLszimbcV@cluster0.vabsxvc.mongodb.net/Attendance-testing?retryWrites=true&w=majority"

uri = 'mongodb+srv://attendance-testing:'+'lq2CXYw7NFX6u6I4'+'@cluster0.9q0pw.mongodb.net/testing-attendance?retryWrites=true&w=majority'

try:
    client = MongoClient(uri,tlsCAFile=certifi.where())
    db = client['testing-attendance']
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    #print(list(db.Employees.find({})))

except Exception as e:
    print(e)