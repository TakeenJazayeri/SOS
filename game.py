import sqlite3
import tkinter as tk
from tkinter import messagebox
import random

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
            admin(record, adminPass)
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
        answer = messagebox.askyesno(title='Signing Out', message='Are you sure?')
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
        tk.Label(master=frame, text='Row nember: ').grid(row=2, column=0, sticky='n')
        entry3 = tk.Entry(master=frame, width=30)
        entry3.grid(row=2, column=1, sticky='n')
        frame.place(x= 20, y=100)

        def checkSecondAccount():
            x = True
            for i in record:
                if i[0] == entry1.get() and i[1] == entry2.get():
                    try:
                        n = int(entry3.get())
                        if n <= 3:
                            entry3.delete(0, len(entry3.get()))
                            messagebox.showinfo(title='ERROR', message='Number of rows should be more than 3.')
                        else:
                            secondSignInWindow.destroy()
                            play(info, i, n)
                    except ValueError:
                        entry3.delete(0, len(entry3.get()))
                        messagebox.showinfo(title='ERROR', message='Number of rows should be an intiger number.')
                    x = False
            if x:
                entry1.delete(0, len(entry1.get()))
                entry2.delete(0, len(entry2.get()))
                messagebox.showinfo(message='Username or password is not correct! Please try again.')

        tk.Button(master=secondSignInWindow, text='Start game', width=12, command=checkSecondAccount).place(x=100, y=180)

    tk.Button(master=dashboardWindow, text='Start new game', height=3, width=30, command=secondSignIn).place(x=90, y=140)
    tk.Button(master=dashboardWindow, text='Edit information', height=2, width=15, command=infoEdit).place(x=85, y=200)
    tk.Button(master=dashboardWindow, text='Change password', height=2, width=15, command=passChange).place(x=200, y=200)
    tk.Button(master=dashboardWindow, text='Exit', height=2, width=15, command=exitD).place(x=85, y=250)
    tk.Button(master=dashboardWindow, text='Sign Out', height=2, width=15, command=signOut).place(x=200, y=250)

    dashboardWindow.mainloop()

def admin (record, adminPass):
    def accountManagement(event):
        selected = event.widget.get(event.widget.curselection()[0])
        for info in record:
            if info[0] == selected:
                break

        adminWindow.destroy()
        
        AMWindow = tk.Tk()
        AMWindow.geometry('350x350')
        AMWindow.resizable(0, 0)

        box = tk.LabelFrame(master=AMWindow, font=('arial', 15), text='User information')
        content = tk.Label(box, font=('arial', 12), text=f'Username: {info[0]}\nFirst name: {info[2]}\nLast name: {info[3]}\nNumber of games: {info[4]}\nNumber of wins: {info[5]}')
        content.pack()
        box.pack(fill=tk.X)

        def editAccount():
            AMWindow.destroy()

            editAccountWindow = tk.Tk()
            editAccountWindow.geometry('310x310')
            editAccountWindow.resizable(0, 0)

            frame = tk.Frame(master=editAccountWindow)
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

                    sqliteConnection.commit()
                    cursor.close()
                    editAccountWindow.destroy()
                    admin(record, adminPass)
                finally:
                    if(sqliteConnection):
                        sqliteConnection.close()
            
            tk.Button(master=editAccountWindow, text='Confirm', width=15, command=edit).place(x=100, y=160)

            editAccountWindow.mainloop()

        def deleteAccount():
            answer = messagebox.askyesno(title='Signing Out', message='Are you sure?')
            if answer:
                try:
                    sqliteConnection = sqlite3.connect('User_Info.db')
                    cursor = sqliteConnection.cursor()

                    query = """DELETE from user_info where user = ?"""
                    cursor.execute(query, (info[0], ))
                    sqliteConnection.commit()

                    selectQuery = "SELECT * FROM user_info"
                    cursor.execute(selectQuery)
                    record = cursor.fetchall()

                    cursor.close()
                    AMWindow.destroy()
                    admin(record, adminPass)
                finally:
                    if(sqliteConnection):
                        sqliteConnection.close()

        def exitAM():
            AMWindow.destroy()
            admin(record, adminPass)

        tk.Button(master=AMWindow, text='Edit account', width=20, command=editAccount).place(x=110, y=160)
        tk.Button(master=AMWindow, text='Delete account', width=20, command=deleteAccount).place(x=110, y=190)
        tk.Button(master=AMWindow, text='Exit', width=20, command=exitAM).place(x=110, y=220)

        AMWindow.mainloop()

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
                elif newpass1.get() == '123456':
                    newpass1.delete(0, len(newpass1.get()))
                    newpass2.delete(0, len(newpass2.get()))
                    messagebox.showerror(title='ERROR', message="Password shouldn't be \"123456\"!")
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
                    newpass = str(newpass1.get())
                    
                    passChangeWindow.destroy()
                    admin(record, newpass)
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()
        
        tk.Button(master=passChangeWindow, text='Confirm', width=15, command=change).place(x=100, y=180)

    def exitA():
        adminWindow.destroy()
        start()
    
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

    tk.Button(master=adminWindow, text='Add a user', width=15, command=addUserAdmin).place(x=70, y=230)
    tk.Button(master=adminWindow, text='Change password', width=15, command=passChange).place(x=70, y=265)
    tk.Button(master=adminWindow, text='Exit', width=15, command=exitA).place(x=70, y=300)
    
    if adminPass == '123456':
        passChange()
        messagebox.showinfo(title='MANDATORY PASSWORD CHANGE', message='Admin should change the password at the first entering.')

    adminWindow.mainloop()

def addUser (isAdmin, record):
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

                selectQuery = "SELECT * FROM admin_info"
                cursor.execute(selectQuery)
                adminPass = cursor.fetchall()[0][0]

                cursor.close()
                addUserWindow.destroy()
                
                if isAdmin == 0:
                    info = newRecord[len(newRecord)-1]
                    dashboard(info)
                if isAdmin == 1:
                    admin(newRecord, adminPass)
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()
                
    tk.Button(master=addUserWindow, text='confirm', width=12, command=enterInfo).place(x=110, y=225)

    addUserWindow.mainloop()

def play (a, b, n):
    global turn, filledCells
    turn = random.randint(0, 1)
    filledCells = 0
    
    class cell:
        def __init__ (self, master, x, y):
            self.x = x
            self.y = y
            self.frame = tk.Frame(master)
            self.frame.grid(row=x, column=y, padx=3, pady=3)

            self.label = tk.Label(master=self.frame, text='', width=2)
            self.label.grid(row=0)

            self.buttonS = tk.Button(master=self.frame, text='S', width=1, command=self.fS)
            self.buttonS.grid(row=0, column=0)
            self.buttonO = tk.Button(master=self.frame, text='O', width=1, command=self.fO)
            self.buttonO.grid(row=0, column=1)

        def fS (self):
            global turn
            self.buttonS.grid_remove()
            self.buttonO.grid_remove()
            self.label.configure(text='S')
            self.label.configure(bg='#2ECC71')
            added(self.x, self.y, 'S')
            
        def fO (self):
            global turn
            self.buttonS.grid_remove()
            self.buttonO.grid_remove()
            self.label.configure(text='O')
            self.label.configure(bg='#3498DB')
            added(self.x, self.y, 'O')
        
        def show (self):
            return self.label['text']
        
        def makeRed (self):
            self.label.configure(bg='#EC7063')
        
        def color (self):
            if turn == 0:
                self.label.configure(bg='#2ECC71')
            if turn == 1:
                self.label.configure(bg='#3498DB')

    def formsSOS (x, y, cellContent):
        global turn
        listNeedToBeRed = []
        if cellContent == 'S':
            if x >= 2:
                if cells[x-1][y].show()=='O' and cells[x-2][y].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x-1][y], cells[x-2][y]])
                if y >= 2 and cells[x-1][y-1].show()=='O' and cells[x-2][y-2].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x-1][y-1], cells[x-2][y-2]])
                if y <= n-3 and cells[x-1][y+1].show()=='O' and cells[x-2][y+2].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x-1][y+1], cells[x-2][y+2]])
            if x <= n-3:
                if cells[x+1][y].show()=='O' and cells[x+2][y].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x+1][y], cells[x+2][y]])
                if y >= 2 and cells[x+1][y-1].show()=='O' and cells[x+2][y-2].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x+1][y-1], cells[x+2][y-2]])
                if y <= n-3 and cells[x+1][y+1].show()=='O' and cells[x+2][y+2].show()=='S':
                    listNeedToBeRed.append([cells[x][y], cells[x+1][y+1], cells[x+2][y+2]])
            if y >= 2 and cells[x][y-1].show()=='O' and cells[x][y-2].show()=='S':
                listNeedToBeRed.append([cells[x][y], cells[x][y-1], cells[x][y-2]])
            if y <= n-3 and cells[x][y+1].show()=='O' and cells[x][y+2].show()=='S':
                listNeedToBeRed.append([cells[x][y], cells[x][y+1], cells[x][y+2]])

        if cellContent == 'O':
            if x >= 1 and x <= n-2 and cells[x-1][y].show()=='S' and cells[x+1][y].show()=='S':
                listNeedToBeRed.append([cells[x-1][y], cells[x][y], cells[x+1][y]])
            if y >= 1 and y <= n-2 and cells[x][y-1].show()=='S' and cells[x][y+1].show()=='S':
                listNeedToBeRed.append([cells[x][y-1], cells[x][y], cells[x][y+1]])
            if x >= 1 and x <= n-2 and y >= 1 and y <= n-2:
                if cells[x-1][y-1].show()=='S' and cells[x+1][y+1].show()=='S':
                    listNeedToBeRed.append([cells[x-1][y-1], cells[x][y], cells[x+1][y+1]])
                if cells[x+1][y-1].show()=='S' and cells[x-1][y+1].show()=='S':
                    listNeedToBeRed.append([cells[x-1][y+1], cells[x][y], cells[x+1][y-1]])

        return listNeedToBeRed

    def added (x, y, cellContent):
        global turn, filledCells
        filledCells += 1
        l = formsSOS(x, y, cellContent)
        scores[turn] += len(l)
        showLabel1()
        if l == []:
            turn = 1 - turn
            showLabel2()
        else:
            for i in l:
                for j in range(3):
                    i[j].makeRed()
        if filledCells == n**2:
            finishedGame()
    
    def showLabel1():
        label1.configure(text=f'{a[0]}: {scores[0]}\t{b[0]}: {scores[1]}')

    def showLabel2():
        if turn == 0:
            label2.configure(text=f"{a[0]}'s turn")
            label2.configure(bg='#2ECC71')
        else:
            label2.configure(text=f"{b[0]}'s turn")
            label2.configure(bg='#3498DB')
    
    def finishedGame():
        if scores[0] > scores[1]:
            messagebox.showinfo(title='!!congratulation!!', message=f'{a[0]} won the game!')
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()

                query = """UPDATE user_info set winNum = ? where user = ?"""
                data = (a[5]+1, a[0])
                cursor.execute(query, data)

                sqliteConnection.commit()
                cursor.close()
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()

        elif scores[0] < scores[1]:
            messagebox.showinfo(title='!!congratulation!!', message=f'{b[0]} won the game!')
            try:
                sqliteConnection = sqlite3.connect('User_Info.db')
                cursor = sqliteConnection.cursor()

                query = """UPDATE user_info set winNum = ? where user = ?"""
                data = (b[5]+1, b[0])
                cursor.execute(query, data)
                
                sqliteConnection.commit()
                cursor.close()
            finally:
                if(sqliteConnection):
                    sqliteConnection.close()

        else:
            messagebox.showinfo(title='!!Draw!!', message='Players have same points!')
        w.destroy()
        start()
    
    def exitP():
        answer = messagebox.askyesno(title='Exit the game', message='Are you sure?')
        if answer:
            w.destroy()
            dashboard(a)
    
    def findSOS():
        for i in range(n):
            for j in range(n):
                if cells[i][j].show() == '':
                    I = formsSOS(i, j, 'S')
                    if not I == []:
                        messagebox.showinfo(title='HELP', message=f"You can fill the cell in row {i+1} column {j+1} with 'S'.")
                        return True
                    I = formsSOS(i, j, 'O')
                    if not I == []:
                        messagebox.showinfo(title='HELP', message=f"You can fill the cell in row {i+1} column {j+1} with 'O'.")
                        return True
        messagebox.showinfo(title='HELP', message="There is no action leading to 'SOS'")
        return False
    
    def guidance0():
        x = int(helpB0['text'][0])
        if x > 0 and turn == 0 and findSOS():
            helpB0.configure(text=str(x-1) + helpB0['text'][1:])
        if x > 0 and turn == 1:
            messagebox.showinfo(title='ERROR', message="It's not the player's turn.")
        if x == 0:
            messagebox.showinfo(title='ERROR', message="The player can't use helps.")
    
    def guidance1():
        x = int(helpB1['text'][0])
        if x > 0 and turn == 1 and findSOS():
            helpB1.configure(text=str(x-1) + helpB1['text'][1:])
        if x > 0 and turn == 0:
            messagebox.showinfo(title='ERROR', message="It's not the player's turn.")
        if x == 0:
            messagebox.showinfo(title='ERROR', message="The player can't use helps.")


    w = tk.Tk()
    w.resizable(0, 0)

    try:
        sqliteConnection = sqlite3.connect('User_Info.db')
        cursor = sqliteConnection.cursor()

        query = """UPDATE user_info set gameNum = ? where user = ?"""
        data1 = (a[4]+1, a[0])
        data2 = (b[4]+1, b[0])

        cursor.execute(query, data1)
        cursor.execute(query, data2)
        sqliteConnection.commit()
        cursor.close()
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
    
    scores = [0, 0]
    label1 = tk.Label(master=w, text='', font=('calibre', 13))
    showLabel1()
    label1.grid(row = 0, pady=3)
    mainframe = tk.Frame(w)
    mainframe.grid(row=2, padx=4, pady=8)

    cells = []
    for i in range(n):
        cells.append([])
    for i in range(n):
        for j in range(n):
            cells[i].append(cell(mainframe, i, j))
    
    
    label2 = tk.Label(master=w, text='', font=('calibre', 13), fg='white')
    label2.grid(row = 1)
    showLabel2()

    frame = tk.Frame(w)
    frame.grid(row=3, pady=2)
    helpB0 = tk.Button(master=frame, text='3 helps', bg='#2ECC71', width=12, height=2, command=guidance0)
    helpB0.grid(row=0, column=0)
    helpB1 = tk.Button(master=frame, text='3 helps', bg='#3498DB', width=12, height=2, command=guidance1)
    helpB1.grid(row=0, column=1)

    tk.Button(master=w, text='Exit', width=12, height=2, command=exitP).grid(row=4, pady=3)


    w.mainloop()


start()