import sqlite3
import tkinter as tk
from tkinter import messagebox

def start():

    try:
        sqliteConnection = sqlite3.connect('User_Info.db')
        cursor = sqliteConnection.cursor()

        selectQuery = "SELECT * FROM admin_info"
        cursor.execute(selectQuery)
        adminPass = cursor.fetchall()[0][0]

        selectQuery = "SELECT * FROM user_info"
        cursor.execute(selectQuery)
        record = cursor.fetchall()
        cursor.close()
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
    
    startWindow = tk.Tk()
    startWindow.geometry('300x300')
    startWindow.resizable(0, 0)

    frame = tk.Frame(master=startWindow)
    label1 = tk.Label(master=frame, text='Username: ').grid(row=0, column=0, sticky='n')
    entry1 = tk.Entry(master=frame, width=30)
    entry1.grid(row=0, column=1, sticky='n')
    label2 = tk.Label(master=frame, text='Password: ').grid(row=1, column=0, sticky='n')
    entry2 = tk.Entry(master=frame, width=30)
    entry2.grid(row=1, column=1, sticky='n')
    frame.place(x= 20, y=100)

    def signIn():
        user = entry1.get()
        pas = entry2.get()
        x = True
        if user=='admin' and pas==str(adminPass):
            messagebox.showinfo(message='You are admin')
            x = False
        else:
            for i in record:
                if i[0] == user and i[1] == pas:
                    messagebox.showinfo(message='You are signed in')
                    x = False
        if x:
            messagebox.showinfo(message='Username or password is not correct! Please try again.')

    signinB = tk.Button(master=startWindow, text='Sign in', width=12, command=signIn)
    signinB.place(x=100, y=150)
    signupB = tk.Button(master=startWindow, text='Sign up', width=12, command=signUp)
    signupB.place(x=100, y=180)
    
    startWindow.mainloop()

def signUp():
    pass

start()