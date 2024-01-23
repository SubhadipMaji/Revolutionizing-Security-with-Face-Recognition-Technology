import cv2
import time


pa_th = "E:/attendance_system/images/"

#List for appending camera images
myList = []

#function for taking picture of student
def take_pic():
    t = input("Enter Your first name: ")
    cap = cv2.VideoCapture(0)
    count = 150
    while count>0:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #show image
        cv2.imshow('img', img)

        myList.append(img)
        
        count -= 1

        # if 'esc' key is being hitted then it will be stopped.
        k = cv2.waitKey(5) & 0xff
        if k == 27:
            break
    
    #counting mid index of myList
    temp = 0
    for i in range(0, len(myList)):
        temp = temp+ i
    mid = temp//len(myList)
    
    #Saving image into file.
    file = pa_th + t + '.jpg'
    cv2.imwrite(file, myList[mid])
    print("Image "+t+" saved")
    
    cap.release()
    
    
# take_pic()