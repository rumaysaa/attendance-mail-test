import face_recognition
import cv2
import numpy as np
import time
from datetime import datetime
import os
from flask import jsonify

def verify_faces(employee_id,path):#username):
    #print(cv2.__version__)
    try:
        if(os.path.exists('./static/encodings/'+employee_id+'.npy')==False):
            #os.remove(path)
            return False
        saved_face_encodings = np.load('./static/encodings/'+employee_id+'.npy')
        video_path = path
        video_capture = cv2.VideoCapture(path)#+cv2.CAP_DSHOW)
        t1 = datetime.now()
        while (datetime.now()-t1).seconds <= 5:
            ret, frame = video_capture.read()
            #print(ret,video_capture.isOpened())
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)

            for encoding in current_face_encodings:
                matches = face_recognition.compare_faces(saved_face_encodings, encoding)
                face_distances = face_recognition.face_distance(saved_face_encodings, encoding)
                #print(matches)
                if True in matches:
                    # Use the minimum distance as the match score
                    match_index = np.argmin(face_distances)
                    match_score = 1 - face_distances[match_index]
                    print(match_score,"match score")
                    if match_score > 0.6:  # Adjust the threshold as needed
                        print(f"Access granted.")# Welcome, {username}! Match Score: {match_score:.2f}")
                        video_capture.release()
                        cv2.destroyAllWindows()
                        return True
        print("Access denied. Face not recognized.")
        video_capture.release()
        cv2.destroyAllWindows()
        return False
    except:
        return False
    
