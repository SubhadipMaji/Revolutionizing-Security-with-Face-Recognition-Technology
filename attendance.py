# **********************************Attandance System***********************************************#


from this import d
import cv2
from cv2 import COLOR_BGR2RGB
import numpy as np
import os
import face_recognition
from datetime import datetime


# dir name where all images are stored. 
path = 'images'

# define empty list for images and name of person.
images = []
PersonName = []

#list of all image names.
myList = os.listdir(path)

# print(myList)

def live_detect():
    #split images and names of myList and appending to images and PersonName lists.
    for current in myList:
        #reading and storing image
        current_image = cv2.imread(f'{path}/{current}')
        images.append(current_image)
        
        #storing person name
        PersonName.append(os.path.splitext(current)[0])
        
    # print(PersonName)

    #Face Encoding: Dlib of face_recognition module basically encodes faces based on 128 different features.so, it find out 128 points from 
    #face.

    #Face Encoding function for n number of faces in a list.
    def FaceEncoding(images):
        #empty list for every encoded images.
        encodeList = []
        
        for img in images:
            #converting BGR format to RGB format.
            img = cv2.cvtColor(img, COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)[0] #HOG Transformation algorithm is used by this module to encode.
            encodeList.append(encodes)
            
        return encodeList

    #stroe output(list of encoded faces) into a variable.
    encodedList = FaceEncoding(images)
    # print("All images encoded successfully.")




    #FOR ATTENDANCE SYSTEM IN CSV
    def attendance(name):
        with open("Attendance.csv", "r+") as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                
            if name not in nameList:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'{name},{tStr},{dStr}\n')

    def detect():
        #Camera Capture feature
        # 0 for laptop camera and 1 for external webcam.
        cap = cv2.VideoCapture(0)

        while True:
            #reading camera Frame
            ret, frame = cap.read()
            #to avoid different resolution values we are putting it into a resize function.
            faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
            #BGR to RGB
            faces = cv2.cvtColor(faces, COLOR_BGR2RGB)
            
            #Find face locations from camera output
            faceCurrentFrame = face_recognition.face_locations(faces)
            #Find face encodings from camera output
            encodeCurrentFrame = face_recognition.face_encodings(faces, faceCurrentFrame)
            
            
            for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
                #compare between encoded list and encode face
                matches = face_recognition.compare_faces(encodedList, encodeFace)
                #face distance calculation
                faceDis = face_recognition.face_distance(encodedList, encodeFace)
                
                #findout minimum distance 
                matchIndex = np.argmin(faceDis)
                
                #check face coming from camera if it is in images directory
                if matches[matchIndex]:
                    na_me = PersonName[matchIndex].upper()
                    # print(na_me)
                    
                    #define face locations.
                    y1,x2,y2,x1 = faceLoc
                    #as we have taken 1/4th in resize function. so we have to multiply be 4.
                    y1,x2,y2,x1 =  y1*4, x2*4, y2*4, x1*4
                    #green border over the face.
                    cv2.rectangle(frame, (x1,y1), (x2,y2),(0,255,0),2)
                    #showing name
                    cv2.rectangle(frame, (x1,y2-35), (x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(frame, na_me, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

                    
                    #calling function for attendance.csv
                    attendance(na_me)
                    
            cv2.imshow("camera", frame)
            if cv2.waitKey(2) == 13:
                break;

        cap.release()
        cv2.destroyAllWindows()
        
    detect()
    
    

        
    
    
