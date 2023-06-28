#Face recognition and attendance management project

import face_recognition
import cv2
import pandas as pd
import sys
import datetime

# Module 1 Reference Data Load Module

ef = pd.read_csv('Student.csv')
stdno = ef["Student No"].tolist()
firstname = ef["First Name"].tolist()
lastname = ef["Last Name"].tolist()
photolocation = ef["Photo Location"].tolist()

n = len(stdno)
std = []
std_encod = []

for i in range(n):
    std.append(face_recognition.load_image_file(photolocation[i]))
    std_encod.append(face_recognition.face_encodings(std[i])[0])

# Module 2 Face Image Capture

camera = cv2.VideoCapture(0)
for i in range(10):
    image = camera.read()
    cv2.imwrite('Student'+str(i)+'.png', image)
del(camera)
uk =face_recognition.load_image_file('Student5.png')

#Module 3 Face Recognition Module

def identify_student(photo):
    try:
        uk_encode = face_recognition.face_encodings(photo)[0]
    except IndexError as e:
        print(e)
        sys.exit(1)

    found = face_recognition.compare_faces(std_encod, uk_encode, tolerance = 0.5)    
    print(found)
    
    index = -1
    for i in range(n):
        if found[i]:
            index = i
    return(index)

std_index = identify_student(uk)    
print(std_index)   

# Module 4 Attendance record in a data file attendance.txt and attendance.csv

sf = pd.read_csv('Attendance.csv')
Stno = sf["Number"].tolist()
date = sf["Date"].tolist()
no=len(Stno)

x1 = str(datetime.datetime.now())
x=x1[0:10]
y=x1[11:]
sno = str(stdno[std_index])
f = firstname[std_index]
l = lastname[std_index]

k=False

for i in range (no):
    if(str(Stno[i])==sno and str(date[i])==x):
        k=True

if (std_index != -1):
    ar = "\n"+sno+" "+f+" "+ l+ "  "+x+" "+y
    if(k==False):
        
        f = open("Attendance.txt", "a")
        f.write(ar)
        f.close() 

        df=pd.DataFrame({'Number':[sno],
                        'First Name':[firstname[std_index]],
                        'Last Name':[l],
                        'Date':[x],
                        'Time':[y]})
        
        df.to_csv('Attendance.csv',mode='a',index=False,header=False)

        print(ar)
    else:
        print(ar,"Your attendance is already taken")

# Module 5 Display Attendance Module

pil_uk = cv2.cvtColor(uk,cv2.COLOR_BGR2RGB)

if std_index ==-1:
    name ="Face NOT Recognized"
else:
    name = firstname[std_index]+" "+lastname[std_index]
x = 150
y = uk.shape[0] -10

faceLoc=face_recognition.face_locations(uk)[0]
cv2.putText(pil_uk,name,(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(123,145,125),1)
cv2.rectangle(pil_uk,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
cv2.imshow('Captured Face',pil_uk)
cv2.waitKey(0)
