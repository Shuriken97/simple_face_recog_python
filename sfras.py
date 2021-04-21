import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import MySQLdb

window = tk.Tk()
window.title("Smart Face Recognition Attendance System")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
 
window.geometry('800x600')
window.configure(background='grey')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="Smart Face Recognition Attendance System" ,bg="blue"  ,fg="white"  ,width=40  ,height=2,font=('times', 20, 'italic bold underline')) 

message.place(x=80, y=20)

lbl = tk.Label(window, text="Enter ID",width=10  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=140, y=130)

txt = tk.Entry(window,width=20  ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=300, y=130)

lbl2 = tk.Label(window, text="Name",width=10  ,fg="red"  ,bg="yellow"    ,height=1 ,font=('times', 15, ' bold ')) 
lbl2.place(x=140, y=170)

txt2 = tk.Entry(window,width=20  ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=300, y=170)

lbl3 = tk.Label(window, text="Matric No",width=10  ,fg="red"  ,bg="yellow"    ,height=1 ,font=('times', 15, ' bold ')) 
lbl3.place(x=140, y=210)

txt3 = tk.Entry(window,width=20  ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
txt3.place(x=300, y=210)

lbl4 = tk.Label(window, text="Notification : ",width=10  ,fg="red"  ,bg="yellow"  ,height=1 ,font=('times', 15, ' bold underline ')) 
lbl4.place(x=90, y=300)

message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=40  ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=220, y=300)

lbl5 = tk.Label(window, text="Attendance : ",width=10  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl5.place(x=90, y=350)

message2 = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=40  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=220, y=350)
 
conn = MySQLdb.connect(host="us-cdbr-east-05.cleardb.net",user="b2bc2043d3485c",password="9a9fcb24",db="heroku_915acf922a70388")

def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)  

def clear3():
    txt3.delete(0, 'end')    
    res = ""
    message.configure(text= res)   
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    matricno=(txt3.get())
    cursor = conn.cursor()
    result = cursor.execute("SELECT * from students where binary name=%s",[name])
    print (result)
    if(result == 1):
	    print("Record Already Present")
    cursor.execute("INSERT INTO students (id,name,matricno) VALUES(%s, %s, %s)",(Id,name,matricno))
    conn.commit()
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                sampleNum=sampleNum+1
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('frame',img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name, matricno]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    message.configure(text= res)

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def Takeattendance():
    def TrackImages():
        sub=tx.get()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("StudentDetails\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Matric No','Subject','Date','Time']
        attendance = pd.DataFrame(columns = col_names)    
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].item()
                    bb=df.loc[df['Id'] == Id]['Matric No'].item()
                    attendance.loc[len(attendance)] = [Id,aa,bb,sub,date,timeStamp]
                    cursor = conn.cursor()
                    result = cursor.execute("SELECT * from attendance where name=%s",[aa])
                    if(result == 1):
                        tt="Attendance taken:"+str(Id)+"-"+aa+"-"+bb
                        cursor.execute("UPDATE attendance SET name = %s, sub_name= %s WHERE name = %s",(aa,sub,aa))
                    else:
                        tt=str(Id)+"-"+aa+"-"+bb
                        cursor.execute("INSERT INTO attendance (name,sub_name) VALUES(%s,%s)",(aa,sub))
                    conn.commit()
                
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+sub+"_"+date+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)
        
    windo = tk.Tk()
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='snow')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="grey", width=33,
                            height=2, font=('times', 15, 'bold'))
    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Take Attendance", fg="white",command=TrackImages, bg="deep pink", width=15, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    fill_a.place(x=300, y=200)

    windo.mainloop()

def open():
    os.system("start C:/Users/Xavier/dev/finalfinaltest/Attendance/")

clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=550, y=120)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=550, y=160)
clearButton2 = tk.Button(window, text="Clear", command=clear3  ,fg="red"  ,bg="yellow"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=550, y=200)       
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=10  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=40, y=450)
trainImg = tk.Button(window, text="Train Dataset", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=10  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=190, y=450)
takeAtn = tk.Button(window, text="Attendance", command=Takeattendance  ,fg="red"  ,bg="yellow"  ,width=10  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeAtn.place(x=340, y=450)
openrep = tk.Button(window, text="Check Report", command=open  ,fg="red"  ,bg="yellow"  ,width=10  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
openrep.place(x=490, y=450)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=10  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=640, y=450)
 
window.mainloop()