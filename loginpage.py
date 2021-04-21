import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from tkinter import filedialog
import MySQLdb

win = tk.Tk()
win.title("Smart Face Recognition Attendance System")
win.configure(background='grey')
win.geometry("500x500")

label_frame_2 = ttk.LabelFrame(win,text = 'Login Form')
label_frame_2.pack(fill=tk.BOTH,padx=15,pady=16)


Login_id = tk.Label(label_frame_2,text="Email Address")
Login_id.grid(row=0,column=0,sticky=tk.W,pady=5)

password = tk.Label(label_frame_2,text ="Password")
password.grid(row=3,column=0,sticky=tk.W,pady=5)

login_var = tk.StringVar()
Login_id_input = tk.Entry(label_frame_2,width=63,textvariable=login_var)
Login_id_input.grid(row=2,column=0,columnspan=5,pady=5,padx=5)
Login_id_input.focus_set()

password_var = tk.StringVar()
password_input = tk.Entry(label_frame_2, show="*",width=63,textvariable=password_var)
password_input.grid(row=4,column=0,columnspan=5,pady=5,padx=5)

def login_func(event=None):
    entered_login = login_var.get()
    entered_password = password_var.get()
    print(f'{entered_login}:{entered_password}')
    conn = MySQLdb.connect(host="us-cdbr-east-05.cleardb.net",user="b2bc2043d3485c",password="9a9fcb24",db="heroku_915acf922a70388")
   
    cursor = conn.cursor()

    query = 'SELECT username,pass FROM admin'
    
    cursor.execute(query)
    counter = 0
    password = []
    username = []
    for i in cursor:
        
        for j in i:
            if counter%2 == 0:
                username.append(j)
            else:
                password.append(j)
            counter += 1
    temp = ''
    wemp = ''
    if entered_login and entered_password:
        for login in username:
            if entered_login == login:
                temp += 'yes'
        
        for p in password:
            if entered_password == p:
                wemp += 'yes'
    else:
        return messagebox.showinfo('Information','Please enter Username and Password')
    
    if len(wemp) > 0 and len(temp) > 0:
        messagebox.showinfo('login','Login Successful')
        Login_id_input.delete(0,tk.END)
        password_input.delete(0,tk.END)
        win.destroy()
        os.system("py sfras.py")
    else:
        messagebox.showerror('Error',f"Either username and password is incorrect!!\n please type correct username and password to Login")
        Login_id_input.delete(0,tk.END)
        password_input.delete(0,tk.END)
    
    query_2 = "SELECT username from admin"
    cursor.execute(query_2)
    for i in cursor:
        print(i)
    
    conn.commit()
    conn.close()



login_btn = ttk.Button(label_frame_2,width=25,text='Login',command=login_func)
login_btn.grid(row=5,column=4,sticky=tk.E,padx=5,pady=40)

win.mainloop()