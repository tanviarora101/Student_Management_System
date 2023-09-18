from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'tanvi' and passwordEntry.get() == '7908':
        messagebox.showinfo('Welcome ', 'Logged in Successfully ')
        window.destroy()
        import system
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')


window = Tk()
window.geometry('1280x650+0+0')
window.resizable(0, 0)
window.title('Login into Student Management System')
bgImg = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(window, image=bgImg)
bgLabel.place(x=0, y=0)

loginFrame = Frame(window, bg='white')  # a container that contains buttons and other labels
loginFrame.place(x=400, y=150)

logoImg = PhotoImage(file='logo.png')

logoLabel = Label(loginFrame, image=logoImg)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

# username entity in login frame
usernameImg = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImg, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=15)
usernameEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=15)

# password entity in login frame
passwordImg = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImg, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=15)
passwordEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, fg='royalblue')
passwordEntry.grid(row=2, column=1, pady=10, padx=15)

# ogin button creation
loginButton = Button(loginFrame, text='Login', font=('times new roman', 15, 'bold'), width=15, bg='cornflowerblue',
                     fg='white', activebackground='cornflowerblue', activeforeground='white',
                     cursor='hand2', command=login)
loginButton.grid(row=3, column=0, columnspan=2, pady=10)

window.mainloop()  # it will keep window on loop so that window is displayed continuously
