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
                    startWindow.destroy()
                    dashboard(i)
                    x = False
        if x:
            entry1.delete(0, len(entry1.get()))
            entry2.delete(0, len(entry2.get()))
            messagebox.showinfo(message='Username or password is not correct! Please try again.')

    signinB = tk.Button(master=startWindow, text='Sign in', width=12, command=signIn)
    signinB.place(x=100, y=150)
    signupB = tk.Button(master=startWindow, text='Sign up', width=12, command=signUp)
    signupB.place(x=100, y=180)
    
    startWindow.mainloop()

def signUp():
    pass

def dashboard(info):
    dashboardWindow = tk.Tk()
    dashboardWindow.geometry('400x450')
    dashboardWindow.resizable(0, 0)

    box = tk.LabelFrame(master=dashboardWindow, font=('arial', 15), text='User information')
    content = tk.Label(box, font=('arial', 12), text=f'Username: {info[0]}\nFirst name: {info[2]}\nLast name: {info[3]}\nNumber of games: {info[4]}\nNumber of wins: {info[5]}')
    content.pack()
    box.pack(fill=tk.X)

    def signOut():
        pass

    def exitD():
        pass

    tk.Button(master=dashboardWindow, text='Start new game', height=3, width=30, command=secondSignIn).place(x=90, y=140)
    tk.Button(master=dashboardWindow, text='Edit information', height=2, width=15, command=infoEdit).place(x=85, y=200)
    tk.Button(master=dashboardWindow, text='Change password', height=2, width=15, command=passChange).place(x=200, y=200)
    tk.Button(master=dashboardWindow, text='Exit', height=2, width=15, command=exitD).place(x=85, y=250)
    tk.Button(master=dashboardWindow, text='Sign Out', height=2, width=15, command=signOut).place(x=200, y=250)

    dashboardWindow.mainloop()

def passChange():
    pass

def secondSignIn():
    pass

def infoEdit():
    pass



start()