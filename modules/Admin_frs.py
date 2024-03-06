import face_recognition
import cv2
import numpy as np
from datetime import datetime
from modules.Config_db import *
import os
from bson.objectid import ObjectId
from bson.binary import Binary
import bson
from bson import json_util

#------not in use-------
def enroll_faces(employee_id):
    #try:
        video_capture = cv2.VideoCapture(0)
        face_encodings = []
        t1 = datetime.now()

        while (datetime.now()-t1).seconds <= 5:
            ret, frame = video_capture.read()
            # Find all face locations and face encodings in the current frame
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)

            for encoding in current_face_encodings:
                face_encodings.append(encoding)

        #cv2.imshow('abcd', frame)
        #Binary(pickle.dumps(np.array(face_encodings), protocol=4), subtype=128 )
        #save_encoodings(employee_id,list(face_encodings))
        np.save('./static/encodings/'+employee_id+'.npy', np.array(face_encodings))
        video_capture.release()
        cv2.destroyAllWindows()
        return True
    #except:
    #    return False


def save_encoodings(userId,enc):
    data = db.Employees.update_one(
        {'_id' : ObjectId(userId) },
        {
        "$set":{ 
            "face_encodings" : enc
    }
        })
    return True

#fetches the saved video and convert in to frames and makes npy file for it
def save_all_frames(employee_id):
    face_encodings = []
    video_path = './static/video/'+employee_id+'.webm'
    cap = cv2.VideoCapture(video_path)
    #check if video is read or not
    if not cap.isOpened():
        return
    frames=[]
    #storing frames from 30th frame in an interval of 2 till 100th frame
    for n in range(1,100,2):
        ret, frame = cap.read()
        if n >=30:
            if ret:
                frames.append(frame)
                face_locations = face_recognition.face_locations(frame)
                current_face_encodings = face_recognition.face_encodings(frame, face_locations)
                for encoding in current_face_encodings:
                    face_encodings.append(encoding)
    #storing the npy file
    np.save('./static/encodings/'+employee_id+'.npy', np.array(face_encodings)) 
    '''db.Encodings.insert_one({
        "employeeID" : ObjectId(employee_id),
        "data" : bson.BSON.encode({'data': json_util.dumps(np.array(face_encodings))})
    })'''
    #print("length of frame",len(frames))
    return frames