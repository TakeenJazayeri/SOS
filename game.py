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
    tk.Label(master=frame, text='Username: ').grid(row=0, column=0, sticky='n')
    entry1 = tk.Entry(master=frame, width=30)
    entry1.grid(row=0, column=1, sticky='n')
    tk.Label(master=frame, text='Password: ').grid(row=1, column=0, sticky='n')
    entry2 = tk.Entry(master=frame, width=30)
    entry2.grid(row=1, column=1, sticky='n')
    frame.place(x= 20, y=100)

    def signIn():
        user = entry1.get()
        pas = entry2.get()
        x = True
        if user=='admin' and pas==str(adminPass):
            startWindow.destroy()
            admin(record)
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

    def signUp():
        startWindow.destroy()
        addUser(0, record)

    signinB = tk.Button(master=startWindow, text='Sign in', width=12, command=signIn)
    signinB.place(x=100, y=150)
    signupB = tk.Button(master=startWindow, text='Sign up', width=12, command=signUp)
    signupB.place(x=100, y=180)
    
    startWindow.mainloop()

def dashboard (info):
    dashboardWindow = tk.Tk()
    dashboardWindow.geometry('400x450')
    dashboardWindow.resizable(0, 0)

    box = tk.LabelFrame(master=dashboardWindow, font=('arial', 15), text='User information')
    content = tk.Label(box, font=('arial', 12), text=f'Username: {info[0]}\nFirst name: {info[2]}\nLast name: {info[3]}\nNumber of games: {info[4]}\nNumber of wins: {info[5]}')
    content.pack()
    box.pack(fill=tk.X)

    def signOut():
        answer = messagebox.askyesno(title='', message='Do you want to sign out?')
        if answer:
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()

                query = """DELETE from user_info where user = ?"""
                cursor.execute(query, (info[0], ))
                sqliteConnection.commit()
                cursor.close()
                exitD()
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()

    def exitD():
        dashboardWindow.destroy()
        start()

    def passChange():
        dashboardWindow.destroy()

        passChangeWindow = tk.Tk()
        passChangeWindow.geometry('320x320')
        passChangeWindow.resizable(0, 0)

        frame = tk.Frame(master=passChangeWindow)
        tk.Label(master=frame, text='Old password: ').grid(row=0, column=0, sticky='n')
        oldpass = tk.Entry(master=frame, width=25)
        oldpass.grid(row=0, column=1, sticky='n')
        tk.Label(master=frame, text='New password: ').grid(row=1, column=0, sticky='n')
        newpass1 = tk.Entry(master=frame, width=25)
        newpass1.grid(row=1, column=1, sticky='n')
        tk.Label(master=frame, text='Repeat new password: ').grid(row=2, column=0, sticky='n')
        newpass2 = tk.Entry(master=frame, width=25)
        newpass2.grid(row=2, column=1, sticky='n')
        frame.place(x= 20, y=100)

        def change():
            if not oldpass.get() == info[1]:
                oldpass.delete(0, len(oldpass.get()))
                messagebox.showerror(title='ERROR', message='Old password is not correct!')
            elif not newpass1.get() == newpass2.get():
                newpass1.delete(0, len(newpass1.get()))
                newpass2.delete(0, len(newpass2.get()))
                messagebox.showerror(title='ERROR', message='Repeated password is not correct!')
            else:
                try:
                    sqliteConnection = sqlite3.connect('User_Info.db')
                    cursor = sqliteConnection.cursor()
                    query = """UPDATE user_info set pass = ? where user = ?"""
                    data = (str(newpass1.get()), info[0])
                    cursor.execute(query, data)
                    sqliteConnection.commit()
                    cursor.close()
                    passChangeWindow.destroy()
                    dashboard(info)
                finally:
                    if(sqliteConnection):
                        sqliteConnection.close()
        
        tk.Button(master=passChangeWindow, text='Confirm', width=15, command=change).place(x=100, y=180)

    def infoEdit():
        dashboardWindow.destroy()

        infoEditWindow = tk.Tk()
        infoEditWindow.geometry('310x310')
        infoEditWindow.resizable(0, 0)

        frame = tk.Frame(master=infoEditWindow)
        tk.Label(master=frame, text='New firstname: ').grid(row=0, column=0, sticky='n')
        fEntry = tk.Entry(master=frame, width=25)
        fEntry.grid(row=0, column=1, sticky='n')
        tk.Label(master=frame, text='New lastname: ').grid(row=1, column=0, sticky='n')
        lEntry = tk.Entry(master=frame, width=25)
        lEntry.grid(row=1, column=1, sticky='n')
        frame.place(x= 20, y=100)

        def edit():
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()

                query1 = """UPDATE user_info set fName = ? where user = ?"""
                data1 = (str(fEntry.get()), info[0])
                cursor.execute(query1, data1)

                query2 = """UPDATE user_info set lName = ? where user = ?"""
                data2 = (str(lEntry.get()), info[0])
                cursor.execute(query2, data2)

                selectQuery = "SELECT * FROM user_info"
                cursor.execute(selectQuery)
                record = cursor.fetchall()
                for i in record:
                    if i[0] == info[0]:
                        x = i

                sqliteConnection.commit()
                cursor.close()
                infoEditWindow.destroy()
                dashboard(x)
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()
        
        tk.Button(master=infoEditWindow, text='Confirm', width=15, command=edit).place(x=100, y=160)

        infoEditWindow.mainloop()

    def secondSignIn():
        dashboardWindow.destroy()

        try:
            sqliteConnection = sqlite3.connect('User_Info.db')
            cursor = sqliteConnection.cursor()
            selectQuery = "SELECT * FROM user_info"
            cursor.execute(selectQuery)
            record = cursor.fetchall()
            cursor.close()
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
        
        secondSignInWindow = tk.Tk()
        secondSignInWindow.geometry('300x300')
        secondSignInWindow.resizable(0, 0)

        frame = tk.Frame(master=secondSignInWindow)
        tk.Label(master=frame, text='Username: ').grid(row=0, column=0, sticky='n')
        entry1 = tk.Entry(master=frame, width=30)
        entry1.grid(row=0, column=1, sticky='n')
        tk.Label(master=frame, text='Password: ').grid(row=1, column=0, sticky='n')
        entry2 = tk.Entry(master=frame, width=30)
        entry2.grid(row=1, column=1, sticky='n')
        frame.place(x= 20, y=100)

        def checkSecondAccount():
            x = True
            for i in record:
                if i[0] == entry1.get() and i[1] == entry2.get():
                    play(info, i)
                    x = False
            if x:
                entry1.delete(0, len(entry1.get()))
                entry2.delete(0, len(entry2.get()))
                messagebox.showinfo(message='Username or password is not correct! Please try again.')

        tk.Button(master=secondSignInWindow, text='Start game', width=12, command=checkSecondAccount).place(x=100, y=150)

    tk.Button(master=dashboardWindow, text='Start new game', height=3, width=30, command=secondSignIn).place(x=90, y=140)
    tk.Button(master=dashboardWindow, text='Edit information', height=2, width=15, command=infoEdit).place(x=85, y=200)
    tk.Button(master=dashboardWindow, text='Change password', height=2, width=15, command=passChange).place(x=200, y=200)
    tk.Button(master=dashboardWindow, text='Exit', height=2, width=15, command=exitD).place(x=85, y=250)
    tk.Button(master=dashboardWindow, text='Sign Out', height=2, width=15, command=signOut).place(x=200, y=250)

    dashboardWindow.mainloop()

def admin (record):
    def accountManagement(event):
        selected = event.widget.get(event.widget.curselection()[0])
        for info in record:
            if info[0] == selected:
                break
        messagebox.showinfo(message=f'This is account of {info[2]} {info[3]}')
    
    adminWindow = tk.Tk()
    adminWindow.geometry('260x400')
    adminWindow.resizable(0, 0)
    
    frame = tk.Frame(adminWindow, height=10)
    frame.place(x=65, y=40)

    users = tk.Listbox(frame, width=20, height=10)
    users.pack(side=tk.LEFT)
    users.bind('<<ListboxSelect>>', accountManagement)

    for i in range(len(record)):
        users.insert(i, record[i][0])

    scroll = tk.Scrollbar(frame, orient='vertical')
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    scroll.config(command=users.yview)
    users.config(yscrollcommand=scroll.set)

    def addUserAdmin():
        adminWindow.destroy()
        addUser(1, record)

    def passChange():
        adminWindow.destroy()

        passChangeWindow = tk.Tk()
        passChangeWindow.geometry('320x320')
        passChangeWindow.resizable(0, 0)

        frame = tk.Frame(master=passChangeWindow)
        tk.Label(master=frame, text='Old password: ').grid(row=0, column=0, sticky='n')
        oldpass = tk.Entry(master=frame, width=25)
        oldpass.grid(row=0, column=1, sticky='n')
        tk.Label(master=frame, text='New password: ').grid(row=1, column=0, sticky='n')
        newpass1 = tk.Entry(master=frame, width=25)
        newpass1.grid(row=1, column=1, sticky='n')
        tk.Label(master=frame, text='Repeat new password: ').grid(row=2, column=0, sticky='n')
        newpass2 = tk.Entry(master=frame, width=25)
        newpass2.grid(row=2, column=1, sticky='n')
        frame.place(x= 20, y=100)

        def change():
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()
                selectQuery = "SELECT * FROM admin_info"
                cursor.execute(selectQuery)
                adminPass = cursor.fetchall()[0][0]

                if not oldpass.get() == adminPass:
                    oldpass.delete(0, len(oldpass.get()))
                    messagebox.showerror(title='ERROR', message='Old password is not correct!')
                elif not newpass1.get() == newpass2.get():
                    newpass1.delete(0, len(newpass1.get()))
                    newpass2.delete(0, len(newpass2.get()))
                    messagebox.showerror(title='ERROR', message='Repeated password is not correct!')
                else:
                    query = """UPDATE admin_info set admin_pass = ?"""
                    data = (str(newpass1.get()), )
                    cursor.execute(query, data)
                    sqliteConnection.commit()
                    cursor.close()
                    passChangeWindow.destroy()
                    admin(record)
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()
        
        tk.Button(master=passChangeWindow, text='Confirm', width=15, command=change).place(x=100, y=180)

    def exitA():
        adminWindow.destroy()
        start()

    tk.Button(master=adminWindow, text='Add a user', width=15, command=addUserAdmin).place(x=70, y=230)
    tk.Button(master=adminWindow, text='Change password', width=15, command=passChange).place(x=70, y=265)
    tk.Button(master=adminWindow, text='Exit', width=15, command=exitA).place(x=70, y=300)

    adminWindow.mainloop()

def play (a, b):
    messagebox.showinfo(message=f'Now yow can play: {a[2]} vs {b[2]}')

def addUser(isAdmin, record):
    addUserWindow = tk.Tk()
    addUserWindow.geometry('310x310')
    addUserWindow.resizable(0, 0)

    frame = tk.Frame(master=addUserWindow)
    frame.place(x= 10, y=100)
    
    tk.Label(master=frame, text='Username: ').grid(row=0, column=0, sticky='n')
    entryU = tk.Entry(master=frame, width=30)
    entryU.grid(row=0, column=1, sticky='n')
    tk.Label(master=frame, text='First name: ').grid(row=1, column=0, sticky='n')
    entryF = tk.Entry(master=frame, width=30)
    entryF.grid(row=1, column=1, sticky='n')
    tk.Label(master=frame, text='Last name: ').grid(row=2, column=0, sticky='n')
    entryL = tk.Entry(master=frame, width=30)
    entryL.grid(row=2, column=1, sticky='n')
    tk.Label(master=frame, text='Password: ').grid(row=3, column=0, sticky='n')
    entryP = tk.Entry(master=frame, width=30)
    entryP.grid(row=3, column=1, sticky='n')
    tk.Label(master=frame, text='Repeat password: ').grid(row=4, column=0, sticky='n')
    entryR = tk.Entry(master=frame, width=30)
    entryR.grid(row=4, column=1, sticky='n')

    def enterInfo():
        exist = False
        u, p, r = entryU.get(), entryP.get(), entryR.get()
        for i in record:
            if i[0] == u:
                exist = True
        if exist or u == 'admin':
            entryU.delete(0, len(u))
            messagebox.showerror(title='ERROR', message='There is a user with same user name!')
        elif not p == r:
            entryP.delete(0, len(p))
            entryR.delete(0, len(r))
            messagebox.showerror(title='ERROR', message='Repeated password is not correct!')
        else:
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()

                query = """INSERT INTO user_info (user, pass, fName, lName, gameNum, winNum) VALUES (?, ?, ?, ?, ?, ?)"""
                data = (str(u), str(p), str(entryF.get()), str(entryL.get()), 0, 0)
                cursor.execute(query, data)
                sqliteConnection.commit()

                selectQuery = "SELECT * FROM user_info"
                cursor.execute(selectQuery)
                newRecord = cursor.fetchall()

                cursor.close()
                addUserWindow.destroy()
                
                if isAdmin == 0:
                    info = newRecord[len(newRecord)-1]
                    dashboard(info)
                if isAdmin == 1:
                    admin(newRecord)
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()
                
    tk.Button(master=addUserWindow, text='confirm', width=12, command=enterInfo).place(x=110, y=225)

    addUserWindow.mainloop()

start()