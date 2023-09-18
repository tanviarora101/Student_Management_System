from tkinter import *
import time
from datetime import datetime
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas as pd


# functionality part
def clock():
    date = time.strftime('%d/%m/%Y')
    currentTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date:{date}\nTime:{currentTime}')
    datetimeLabel.after(1000, clock)


# TO EXIT THE PROJECT
def exitSystem():
    result = messagebox.askyesno('Confirm Exit', 'Are you sure you want to exit ?')
    if result:
        root.destroy()
    else:
        pass


# EXPORT DATA FROM TREEVIEW TO EXCEL FILE PART
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newList = []
    for i in indexing:
        data = studentTable.item(i)
        dataList = data['values']
        newList.append(dataList)

    table = pd.DataFrame(newList, columns=['Id', 'Name', 'DOB', 'Gender', 'Phn no.', 'Email', 'City', 'Entry Date'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Data Exported', 'Data Exported and saved successfully')


# buttons functioning
def addStudent():
    def addData():
        # checking whether all inputs are filled or not
        if idEntry.get() == '' or NameEntry.get() == '' or dobEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or phoneEntry.get() == '' or genderEntry.get() == '':
            messagebox.showerror('error', 'All Fields are required', parent=addStudWindow)
        else:
            currentDate = time.strftime('%Y/%m/%d')
            id = idEntry.get()
            name = NameEntry.get()
            dob = datetime.strptime(dobEntry.get(), '%d/%m/%Y')  # converted into date-time object
            dob_sqlFormat = dob.strftime('%Y/%m/%d')  # date that will be entered in format - YYYY-MM-DD
            gen = genderEntry.get()
            phn = phoneEntry.get()
            mail = emailEntry.get()
            city = addressEntry.get()

            try:
                query = 'insert into students (id,name,d_o_b,gender,Contact,E_mail,city,entry_date) values (%s,%s,%s,%s,%s,%s,%s,%s);'
                mycursor.execute(query, (id, name, dob, gen, phn, mail, city, currentDate))
                con.commit()
                messagebox.showinfo('Database Updated', 'Data Added Successfully', parent=addStudWindow)
                ans = messagebox.askyesno('clear', 'clear form')
                if ans:
                    idEntry.delete(0, END)
                    NameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    dobEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    addressEntry.delete(0, END)
                else:
                    pass

            except:
                messagebox.showerror('Found Duplicate values', 'Id already exists', parent=addStudWindow)
                return

            query = 'select * from students'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                dataList = list(data)
                studentTable.insert('', END, values=(dataList))

    # creating the window of add student
    addStudWindow = Toplevel()
    addStudWindow.title('Add Student')
    addStudWindow.grab_set()
    addStudWindow.geometry('400x535+50+50')
    addStudWindow.resizable(False, False)
    idLabel = Label(addStudWindow, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid()
    idEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    idEntry.grid(row=0, column=1, padx=20, pady=20)

    NameLabel = Label(addStudWindow, text='Name', font=('times new roman', 20, 'bold'))
    NameLabel.grid()
    NameEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    NameEntry.grid(row=1, column=1, padx=20, pady=20)

    dobLabel = Label(addStudWindow, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid()
    dobEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    dobEntry.grid(row=2, column=1, padx=20, pady=20)

    genderLabel = Label(addStudWindow, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid()
    genderEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    genderEntry.grid(row=3, column=1, padx=20, pady=20)

    phoneLabel = Label(addStudWindow, text='Contact', font=('times new roman', 20, 'bold'))
    phoneLabel.grid()
    phoneEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    phoneEntry.grid(row=4, column=1, padx=20, pady=20)

    emailLabel = Label(addStudWindow, text='E-mail ID', font=('times new roman', 20, 'bold'))
    emailLabel.grid()
    emailEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    emailEntry.grid(row=5, column=1, padx=20, pady=20)

    addressLabel = Label(addStudWindow, text='City', font=('times new roman', 20, 'bold'))
    addressLabel.grid()
    addressEntry = Entry(addStudWindow, font=('times new roman', 15, 'bold'), bd=1)
    addressEntry.grid(row=6, column=1, padx=20, pady=20)

    submitButton = ttk.Button(addStudWindow, text='Submit', command=addData)
    submitButton.grid(row=7, columnspan=2, pady=10)
    # end of add student function


# SEARCH STUDENT BUTTON FUNCTIONING
def searchStudent():
    def searchData():
        # dob = datetime.strptime(dobEntry.get(), '%d/%m/%Y')  # converted into date-time object
        # dob_sqlFormat = dob.strftime('%Y-%m-%d')  # date that will be entered in format - YYYY-MM-DD
        query = 'select * from students where id=%s or name=%s or gender=%s or e_mail=%s or city=%s'
        mycursor.execute(query,
                         (idEntry.get(), NameEntry.get(), genderEntry.get(), emailEntry.get(), addressEntry.get()))
        studentTable.delete(*studentTable.get_children())
        fetched_data = mycursor.fetchall()
        for d in fetched_data:
            studentTable.insert('', END, values=d)

    searchWindow = Toplevel()
    searchWindow.grab_set()
    searchWindow.title('Search Student')
    searchWindow.geometry('400x420+50+50')
    searchWindow.resizable(0, 0)
    idLabel = Label(searchWindow, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid()
    idEntry = Entry(searchWindow, font=('times new roman', 15, 'bold'), bd=1)
    idEntry.grid(row=0, column=1, padx=20, pady=20)

    NameLabel = Label(searchWindow, text='Name', font=('times new roman', 20, 'bold'))
    NameLabel.grid()
    NameEntry = Entry(searchWindow, font=('times new roman', 15, 'bold'), bd=1)
    NameEntry.grid(row=1, column=1, padx=20, pady=20)

    genderLabel = Label(searchWindow, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid()
    genderEntry = Entry(searchWindow, font=('times new roman', 15, 'bold'), bd=1)
    genderEntry.grid(row=2, column=1, padx=20, pady=20)

    emailLabel = Label(searchWindow, text='E-mail ID', font=('times new roman', 20, 'bold'))
    emailLabel.grid()
    emailEntry = Entry(searchWindow, font=('times new roman', 15, 'bold'), bd=1)
    emailEntry.grid(row=3, column=1, padx=20, pady=20)

    addressLabel = Label(searchWindow, text='City', font=('times new roman', 20, 'bold'))
    addressLabel.grid()
    addressEntry = Entry(searchWindow, font=('times new roman', 15, 'bold'), bd=1)
    addressEntry.grid(row=4, column=1, padx=20, pady=20)

    searchButton = ttk.Button(searchWindow, text='Search', command=searchData)
    searchButton.grid(row=5, columnspan=2, pady=10)


# DELETE STUDENT BUTTON FUNCTIONALITY
def delStudent():
    index = studentTable.focus()
    print(index)
    content = studentTable.item(index)
    content_id = content['values'][0]
    query = 'delete from students where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Database Updated', f'Id {content_id} deleted successfully')
    showStd()


# SHOW STUDENT BUTTON FUNCTIONALITY PART
def showStd():
    query = 'select * from students'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


# MODIFY STUDENT FUNCTIONING PART HERE
def modifyStudent():
    def updateData():
        currentDate = time.strftime('%Y-%m-%d')
        dob = datetime.strptime(dobEntry.get(), '%d/%m/%Y')  # converted into date-time object
        dob_sqlFormat = dob.strftime('%Y-%m-%d')  # date that will be entered in format - YYYY-MM-DD
        query = 'update students set name=%s, D_O_B=%s, gender=%s, Contact=%s, E_mail=%s, city=%s, entry_date=%s where id=%s'
        mycursor.execute(query, (
            NameEntry.get(), dob_sqlFormat, genderEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
            currentDate, idEntry.get()))
        con.commit()
        messagebox.showinfo('Modified', f'Id {idEntry.get()} Modified Successfully', parent=modifyWindow)
        modifyWindow.destroy()
        showStd()

    modifyWindow = Toplevel()
    modifyWindow.title('Modify Student')
    modifyWindow.grab_set()
    modifyWindow.geometry('400x535+50+50')
    modifyWindow.resizable(0, 0)

    idLabel = Label(modifyWindow, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid()
    idEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    idEntry.grid(row=0, column=1, padx=20, pady=20)

    NameLabel = Label(modifyWindow, text='Name', font=('times new roman', 20, 'bold'))
    NameLabel.grid()
    NameEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    NameEntry.grid(row=1, column=1, padx=20, pady=20)

    dobLabel = Label(modifyWindow, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid()
    dobEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    dobEntry.grid(row=2, column=1, padx=20, pady=20)

    genderLabel = Label(modifyWindow, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid()
    genderEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    genderEntry.grid(row=3, column=1, padx=20, pady=20)

    phoneLabel = Label(modifyWindow, text='Contact', font=('times new roman', 20, 'bold'))
    phoneLabel.grid()
    phoneEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    phoneEntry.grid(row=4, column=1, padx=20, pady=20)

    emailLabel = Label(modifyWindow, text='E-mail ID', font=('times new roman', 20, 'bold'))
    emailLabel.grid()
    emailEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    emailEntry.grid(row=5, column=1, padx=20, pady=20)

    addressLabel = Label(modifyWindow, text='City', font=('times new roman', 20, 'bold'))
    addressLabel.grid()
    addressEntry = Entry(modifyWindow, font=('times new roman', 15, 'bold'), bd=1)
    addressEntry.grid(row=6, column=1, padx=20, pady=20)

    modifyButton = ttk.Button(modifyWindow, text='Modify', command=updateData)
    modifyButton.grid(row=7, columnspan=2, pady=10)

    index = studentTable.focus()
    # print(index)
    content = studentTable.item(index)
    data = content['values']
    print(data)
    idEntry.insert(0, data[0])
    NameEntry.insert(0, data[1])
    dobEntry.insert(0, data[2])
    genderEntry.insert(0, data[3])
    phoneEntry.insert(0, data[4])
    emailEntry.insert(0, data[5])
    addressEntry.insert(0, data[6])


# FUNCTION THAT WILL CONNECT TO THE DATABSE
def connect_db():
    # CONNECTING TO THE DATABASE
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid details', parent=root)
            return

        query = 'use sms'
        mycursor.execute(query)
        messagebox.showinfo('Connected', 'Connected to Database Successfully', parent=root)
        dbWindow.destroy()

    showStudent.config(state=NORMAL)
    addStudent.config(state=NORMAL)
    searchStudent.config(state=NORMAL)
    deleteStudent.config(state=NORMAL)
    exitButton.config(state=NORMAL)
    exportData.config(state=NORMAL)
    modifyStudent.config(state=NORMAL)

    dbWindow = Toplevel()
    dbWindow.grab_set()
    dbWindow.geometry('470x250+730+230')
    dbWindow.title('Database Connection')
    dbWindow.resizable(0, 0)

    # CREATING THE HOST ENTRY LABEL IN DB CONNECTION WINDOW
    hostLabel = Label(dbWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostLabel.grid(row=0, column=0, padx=20)
    hostEntry = Entry(dbWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    # CREATING THE USER ENTRY WINDOW
    user = Label(dbWindow, text='User Name', font=('arial', 20, 'bold'))
    user.grid(row=1, column=0, padx=20)
    userEntry = Entry(dbWindow, font=('roman', 15, 'bold'), bd=2)
    userEntry.grid(row=1, column=1, padx=40, pady=20)

    # CREATING THE PASSWORD ENTRY LABEL FOR DATABASE CONNECTION
    password = Label(dbWindow, text='Password', font=('arial', 20, 'bold'))
    password.grid(row=2, column=0, padx=20)
    passwordEntry = Entry(dbWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    # CREATE A CONNECT TO DB BUTTON
    dbConnectButton = ttk.Button(dbWindow, text='Connect', command=connect)
    dbConnectButton.grid(row=3, columnspan=2)


count = 0
text = ""


def slider():
    global text, count
    if count == len(s):
        return
    text = text + s[count]
    sliderLabel.config(text=text)
    count = count + 1
    sliderLabel.after(200, slider)


# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

# TIME AND DATE AT TOP LEFT CORNER OF THE ROOT WINDOW
datetimeLabel = Label(root, font=('times new roman', 15, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()  # CALL TO THE FUNCTION CLOCK

# TOP HEADING OF SMS
s = 'Student Management System'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=35)
sliderLabel.place(x=200, y=0)
slider()

# CREATING THE BUTTON THAT CONNECTS TO THE DATABASE
connectButton = ttk.Button(root, text='Connect to Database', command=connect_db)
connectButton.place(x=980, y=0)

# WHOLE LEFT FRAME OF THE ROOT WINDOW WITH BUTTONS
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

left_image = PhotoImage(file='student (1).png')
left_label = Label(leftFrame, image=left_image)
left_label.grid(row=0, column=0)

addStudent = ttk.Button(leftFrame, text="Add Student", width=25, state=DISABLED, command=addStudent)
addStudent.grid(row=1, column=0, pady=13)

searchStudent = ttk.Button(leftFrame, text="Search Student", width=25, state=DISABLED, command=searchStudent)
searchStudent.grid(row=2, column=0, pady=20)

deleteStudent = ttk.Button(leftFrame, text="Delete Student", width=25, state=DISABLED, command=delStudent)
deleteStudent.grid(row=3, column=0, pady=20)

modifyStudent = ttk.Button(leftFrame, text="Modify Student", width=25, state=DISABLED, command=modifyStudent)
modifyStudent.grid(row=4, column=0, pady=20)

showStudent = ttk.Button(leftFrame, text="Show Student", width=25, state=DISABLED, command=showStd)
showStudent.grid(row=5, column=0, pady=20)

exportData = ttk.Button(leftFrame, text="Export Data", width=25, state=DISABLED, command=export_data)
exportData.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text="Exit", width=25, state=DISABLED, command=exitSystem)
exitButton.grid(row=7, column=0, pady=20)

# RIGHT FRAME OF THE ROOT WINDOW
rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

# CREATING THE SCROLL BARS FOR THE TABLE TREE VIEW
scrollX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollY = Scrollbar(rightFrame, orient=VERTICAL)

# CREATING THE TABLE TREE VIEW
studentTable = ttk.Treeview(rightFrame, columns=(
    'Id', 'Name', 'D.O.B', 'Gender', 'Contact no.', 'E-mail Id', 'City', 'Date added'),
                            xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
scrollX.config(command=studentTable.xview)
scrollY.config(command=studentTable.yview)

scrollX.pack(side=TOP, fill=X)
scrollY.pack(side=RIGHT, fill=Y)
studentTable.pack()

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Gender', text='Gender')
studentTable.heading('Contact no.', text='Contact no.')
studentTable.heading('E-mail Id', text='E-mail Id')
studentTable.heading('City', text='City')
studentTable.heading('Date added', text='Entry date')

# STYLING THE TREE VIEW OF STUDENT
studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=350, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Gender', width=170, anchor=CENTER)
studentTable.column('Contact no.', width=240, anchor=CENTER)
studentTable.column('E-mail Id', width=300, anchor=CENTER)
studentTable.column('City', width=200, anchor=CENTER)
studentTable.column('Date added', width=200, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=35, font=('arial', 15, 'bold'), background='pink', foreground='black',
                fieldbackground='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'))

studentTable.config(show='headings')
root.mainloop()
