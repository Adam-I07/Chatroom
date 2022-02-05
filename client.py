import socket
import threading
from tkinter import *
import sys
from tkinter import messagebox
import csv
from csv import DictReader
import datetime

import encryption
import passwordEncryption

'''Assigning the port number and host address. Creating the socket and binding the address to that socket'''
port = 50000
host = "127.0.0.1"
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host, port))

'''Main class used to create the chatroom and functions'''
class chatroom:
    '''Creates the first tkinter window with buttons and labels.This is the "Menu" which will display once
    the client is connected allowing the user to "Join as guest", "login" or "Register"'''
    def __init__(self):
        self.chatRoom = Tk()
        self.chatRoom.withdraw()

        self.startWindow = Toplevel()
        self.startWindow.title("Chatroom")
        self.startWindow.resizable(width=False,
                                   height=False)
        self.startWindow.configure(width=300,
                                   height=200,
                                   bg="#000000")
        self.startWindowTitle = Label(self.startWindow,text="Choose a method to join",font=('Ariel', 12),bg="#000000",fg="#fff")
        self.startWindowTitle.place(relheight=0.10,relx=0.2,rely=0.08)

        self.loginButton = Button(self.startWindow, text="Login", font=('Ariel', 10), command=self.loginWindow)
        self.loginButton.place(relx=0.5, rely=0.35, height = "30", width = "200", anchor = CENTER)

        self.joinAsGuestButton = Button(self.startWindow,text="Join as guest",font=('Ariel', 10),command= self.joinAsGuest)
        self.joinAsGuestButton.place(relx=0.5, rely=0.58, height="30", width="200",anchor = CENTER)

        self.regButton = Button(self.startWindow, text="Register", font=('Ariel', 10), command=self.regWindow)
        self.regButton.place(relx=0.5, rely=0.8, height="30", width="200", anchor=CENTER)

        self.startWindow.mainloop()
    '''If the client chooses join as guest this function will close the main menu and open this form which is the 
    joinAsGuest allowing the user to enter a username in a text box and click join'''
    def joinAsGuest(self):
        self.startWindow.destroy()
        self.guestJoin = Toplevel()
        self.guestJoin.title("Join chat room")
        self.guestJoin.geometry('300x150')
        self.guestJoin.configure(bg="#000000")

        self.enterUsername = Label(self.guestJoin, text="Enter a username:", font=('Ariel', 10), bg="#000000", fg="#fff")
        self.enterUsername.place(x=10, y=35)

        self.labelName = Label(self.guestJoin, text="Username: ", font=('Ariel', 9), bg="#000000", fg="#fff")
        self.labelName.place(x=10, y=75)

        self.entryName = Entry(self.guestJoin, font=('Ariel', 14), width=12, bg="#fff")
        self.entryName.place(x=83, y=72)
        self.entryName.focus()

        self.joinButton = Button(self.guestJoin, text="Join", font=('Ariel', 10), command=lambda: self.joinMainRoomAsGuest(self.entryName.get()))
        self.joinButton.place(x=225, y=70)
        self.guestJoin.mainloop()
    ''''This function is linked with the "join" button on the joinAsGuest Window and will take the user compare it with
    the users in the login details file of existing users and also with other guests currently in the room. If the 
    username enteres already exists the client will get a messagebox telling them to pick again, else it will start a 
    thread to the "joinMainRoom" function'''
    def joinMainRoomAsGuest(self, username):
        file = open('loginDetails.csv', 'r')
        currentUser = DictReader(file)
        usernamesUsed = []
        for row in currentUser:
            ldetails = []
            ldetails.append(row['Username'])
            usernamesUsed.append(ldetails)
        usernamesCurrent = []
        currentUsernameInputted = (username.lower())
        if username != '':
            for i in usernamesUsed:
                usernamesCurrent.append(i[0])

            if currentUsernameInputted in usernamesCurrent:
                doesExist = True
            else:
                doesExist = False
            if doesExist == True:
                messagebox.showerror('Register', f'{username} Already Exist.')
            else:
                self.mainRoom()
                startThread = threading.Thread(target=self.joinMainRoom)
                self.username = username
                startThread.start()
                self.guestJoin.destroy()
    '''This creates the login form if the user wants to log in'''
    def loginWindow(self):
        self.startWindow.destroy()
        # if(self.registerWindow.state is True):
        #     self.registerWindow.destroy()
        self.loginJoin = Toplevel()
        self.loginJoin.title("Log in")
        self.loginJoin.geometry('300x300')
        self.loginJoin.resizable(0,0)
        self.loginJoin.configure(bg='black')

        self.loginLabel = Label(self.loginJoin,text='Login',width=20,height=1,font=('Ariel', 20, 'bold'),bg="#000000",fg="#fff")
        self.loginLabel.pack()

        self.usernameLabel = Label(self.loginJoin,text='Username :',font=('Arial', 14, 'bold'),bg="#000000",fg="#fff")
        self.usernameLabel.place(x=10,y=50)

        self.user_entry = Entry(self.loginJoin,font=('Arial', 10, 'bold'),width=25,bg='#fff')
        self.user_entry.place(x=10, y=80)

        self.passwordLabel = Label(self.loginJoin,text='Password :', font=('Arial', 14, 'bold'), bg="#000000",fg="#fff")
        self.passwordLabel.place(x=10, y=110)

        self.pass_entry = Entry(self.loginJoin,show='*',font=('Arial', 10, 'bold'),width=25, bg='white')
        self.pass_entry.place(x=10, y=140)

        self.login = Button(self.loginJoin,text='Login',font=('Arial', 10, 'bold'), width=14,bg='green',bd=0,fg='white',command=lambda: self.loginCheck(self.user_entry.get(), self.pass_entry.get()))
        self.login.place(x=10, y=180)

    '''This function is linked to button on the login form called "Login". It will take the log in details inputted by
    the user store them to 2 variable. It will open the csv files with all the usernames and password and comapare 
    all the usernames and passwords in the file to the ones inputted by the user. If it is wrong it will display a 
    message box telling the user they have entered the wrong details else it will start a thread targeting the 
    "joinMainRoom"'''
    def loginCheck(self,username, password):
        file = open('loginDetails.csv', 'r')
        details = DictReader(file)
        loginInputDetails = []
        for row in details:
            loginDetails = []
            loginDetails.append(row['Username'])
            loginDetails.append(row['Password'])
            loginInputDetails.append(loginDetails)

        inputtedUser = (username.lower())
        inputtedPass = password


        loginSuccessful = False

        for i in loginInputDetails:

            if i[0] == inputtedUser:
                passw = i[1]
                decryptedPass = passwordEncryption.decrypt(passw)
                if inputtedPass == decryptedPass:
                    loginSuccessful = True
                    self.mainRoom()
                    startThread = threading.Thread(target=self.joinMainRoom)
                    self.username = inputtedUser
                    startThread.start()
                    self.loginJoin.destroy()
                    break
            else:
                loginSuccessful = False

        if loginSuccessful == True:
            messagebox.showinfo("Log in", "You have successfuly logged in")
        else:
            messagebox.showerror("Log in unsuccessful", "You have entered the wrong details try again!")

    '''This Creates a register form for the user if they choose to register'''
    def regWindow(self):
        self.startWindow.destroy()
        self.registerWindow = Tk()
        self.registerWindow.title('Register')
        self.registerWindow.configure( bg='#000000')
        self.registerWindow.geometry('300x300+220+170')
        self.registerWindow.resizable(0, 0)

        self.reg_label = Label(self.registerWindow, text='Register', fg='white',bg='#000000', width=20, height=1, font=('Arial', 20, 'bold'))
        self.reg_label.pack()

        self.Username_Label = Label(self.registerWindow, text='Username :',fg='white', font=('Arial', 14, 'bold'),  bg='#000000')
        self.Username_Label.place(x=10, y=50)

        self.username_entry = Entry(self.registerWindow, font=('Arial', 10, 'bold'), width=25, bg='white')
        self.username_entry.place(x=10, y=80)

        self.password_Label = Label(self.registerWindow, text='Password :',fg='white', font=('Arial', 14, 'bold'), bg='#000000')
        self.password_Label.place(x=10, y=110)

        self.password_entry = Entry(self.registerWindow, font=('Arial', 10, 'bold'), width=25, bg='white')
        self.password_entry.place(x=10, y=140)

        self.submitButton = Button(self.registerWindow, text='Submit', font=('Arial', 10, 'bold'), width=14, bg='green', command=lambda: self.regFunction(self.username_entry.get(), self.password_entry.get()),bd=0, fg='white')
        self.submitButton.place(x=10, y=180)

        self.GoToLoginLabel = Label(self.registerWindow, text='Already have an account',fg='white', bg='#000000')
        self.GoToLoginLabel.place(x=30, y=215)

        self.LoginFormButton = Button(self.registerWindow, text='Log_In', font=('Arial', 10, 'underline'), fg='blue', command=lambda: self.loginWindow())
        self.LoginFormButton.place(x=170, y=210)

    '''This button is linked to the LoginFormButton in the register window. once clicked it will open the csv file
    store all the login details in there. Then it will get the details inputted by the user and store them to local
    variables. all usernames are stored as lowercase to stop duplicate uppercase users being created. It will
    check first to see if the user already exists if it does already exist the user will get a messagebox error telling
    them to change the username else it will create a new user in the directory and ask them to go log in'''
    def regFunction(self, username, password):
        file = open('loginDetails.csv', 'r')
        register = DictReader(file)
        loginDetailsInputted = []
        for row in register:
            ldetails = []
            ldetails.append(row['Username'])
            ldetails.append(row['Password'])
            loginDetailsInputted.append(ldetails)

        currentUser = username.lower()
        currentPass = password
        encryptedPass = passwordEncryption.encrypt(currentPass)


        if currentUser != '' and currentPass != '':

            newUsername = []
            for i in loginDetailsInputted:
                newUsername.append(i[0])

            if currentUser in newUsername:
                doesExist = True
            else:
                doesExist = False

            if doesExist == True:
                messagebox.showerror('Register', f'{currentUser} Already Exist.')
            else:
                writeToCSV = [currentUser, encryptedPass]
                with open('loginDetails.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(writeToCSV)

                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)
                messagebox.showinfo('Register', f'{currentUser} successfuly registered. Click the log in button to go login and chat!.')

    '''This function gets the current local time of the client'''
    def currentTime(self):
        # gets the time in the Hours:Minutes format
        now = datetime.datetime.now()
        formattedTime = now.strftime("%H:%M")
        return formattedTime

    '''This method joins the client to the main room then waits to  recieves commands from the server and 
    does what it says'''
    def joinMainRoom(self):
        print(f'{self.username} has joined the chatroom')
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                decryptedMessage = encryption.clientEncryption.decryptMessage(message)
                if decryptedMessage == 'SendUsername':
                    name = self.username
                    encryptedUsername = encryption.clientEncryption.encryptMessage(name)
                    client.send(encryptedUsername.encode('utf-8'))
                elif 'new/txtbg/col/accepted' in decryptedMessage:
                    col = decryptedMessage.split('+')[1]
                    print('col')
                    self.textCons.config(state=NORMAL)
                    self.textCons.config(bg=col)
                    self.textCons.config(state=DISABLED)
                elif 'new/txtfg/col/accepted' in decryptedMessage:
                    col = decryptedMessage.split('+')[1]
                    self.textCons.config(state=NORMAL)
                    self.textCons.config(fg=col)
                    self.textCons.config(state=DISABLED)
                elif 'new/bg/col/accepted' in decryptedMessage:
                    col = decryptedMessage.split('+')[1]
                    print(col)
                    self.chatRoom.config(bg=col)
                elif decryptedMessage == 'new/col/declined':
                    messagebox.showerror("Invalid Colour", "The colour was invalid try again")
                elif decryptedMessage == '/user|close|command':
                    print("You have left the room")
                    messagebox.showinfo("Goodbye", "Come back soon.")
                    self.chatRoom.destroy()
                    client.close()
                    sys.exit()
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,"[{}] {} \n".format(self.currentTime(), decryptedMessage))

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("{} has left the chatroom".format(self.username))
                break

    '''This method sends the command to leave the chat to the server'''
    def leaveMainRoom(self):
        leaveCommand = '/user|leave/room'
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(leaveCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))

    '''This method sends the command to show all users to the server'''
    def showAllOnlineUsers(self):
        showUsersCommand = '/users|Show/online/users'
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(showUsersCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))

    '''This method clears the chat at the users request'''
    def clearChat(self):
        self.textCons.config(state=NORMAL)
        self.textCons.delete(1.0, END)
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    '''This method sends the command to show the current date and time to the server'''
    def currentDateAndTime(self):
        getDateAndTimeCommand = '/users|Show/current/date/time'
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(getDateAndTimeCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))

    '''This method creates the chatroom the users use to send messages to eachother'''
    def mainRoom(self):
        self.chatRoom.deiconify()
        self.chatRoom.title("Chatroom")
        self.chatRoom.geometry('530x400')
        self.chatRoom.resizable(0, 0)
        self.chatRoom.title("Chatroom")
        self.chatRoom.configure(bg="#000000")

        self.chatLabel = Label(self.chatRoom, text='Chatroom', bg="#000000",fg='#fff', font=('Arial', 13, 'bold'), width=10, height=1).pack()

        '''The chat box that displays the messages sent by the users'''
        self.textCons = Text(self.chatRoom, width=54, height=19,  bg="#000000", fg='#fff', font=('arial', 10))
        self.textCons.place(x=10, y=40)

        self.leaveRoomButton = Button(self.chatRoom, text='Leave', font=('Arial', 10), command = lambda: self.leaveMainRoom())
        self.leaveRoomButton.place(x=400, y=15, height=40, width=125)

        self.showOnlineUsersButton = Button(self.chatRoom, text='Show Online Users', font=('Ariel', 10), command= lambda : self.showAllOnlineUsers())
        self.showOnlineUsersButton.place(x=400, y=65, height=40, width=125)

        self.showCurrentDateButton = Button(self.chatRoom, text='Get Date and Time', font=('Ariel', 10),command=lambda: self.currentDateAndTime())
        self.showCurrentDateButton.place(x=400, y=115, height=40, width=125)

        self.clearChatButton = Button(self.chatRoom, text='Clear Chat', font=('Ariel', 10), command= lambda : self.clearChat())
        self.clearChatButton.place(x=400, y= 165, height=40, width=125)

        self.editChatRoomButton = Button(self.chatRoom, text='Edit Chat', font=('Ariel', 10),command=lambda: self.editChat())
        self.editChatRoomButton.place(x=400, y=215, height=40, width=125)

        self.entryMsg  = Entry(self.chatRoom, font=('arial black', 13), width=25)
        self.entryMsg.place(x=10, y=365)
        self.entryMsg.focus()

        self.sendMessageButton = Button(self.chatRoom, font=('arial', 10), text='Send', bd=0, bg='blue', fg='white', width=10, command=lambda: self.sendButton(self.entryMsg.get()))
        self.sendMessageButton.place(x=300, y=365)

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.970)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    '''This function is linked to the "editChatRoomButton int he mainRoom and allows the user to change the colour scheme
    of the chat room by allowing them to input colour name'''
    def editChat(self):
        self.editTextWindow = Tk()
        self.editTextWindow.title('Register')
        self.editTextWindow.configure(bg='#000000')
        self.editTextWindow.geometry('350x310')
        self.editTextWindow.resizable(0, 0)
        self.windowTitle = Label(self.editTextWindow, text="Edit Chatroom Asthetics", fg="white",font=('Arial', 20, 'bold'), bg="black")
        self.windowTitle.place(x=10,y=0)

        self.changeBackgroundLabel = Label(self.editTextWindow, text="Enter colour to change the background:",fg="white", font=('Arial', 10, 'bold'), bg="black", width=50)
        self.changeBackgroundLabel.place(x=-70, y=45)
        self.changeBackgroundEntry = Entry(self.editTextWindow, font=('Arial', 10, 'bold'), width=25, bg='white')
        self.changeBackgroundEntry.place(x=5, y=75)
        self.changeBackgroundButton = Button(self.editTextWindow, text='Change Background \nColour', font=('Ariel', 10),command=lambda: self.changeBGColourFunc(self.changeBackgroundEntry.get()))
        self.changeBackgroundButton.place(x=195, y=70,  height=40, width=130)

        self.changeTextBackgroundLabel = Label(self.editTextWindow, text="Enter colour to change the text background:",fg="white",font=('Arial', 10, 'bold'),  bg="black", width=50)
        self.changeTextBackgroundLabel.place(x=-58, y=120)
        self.changeTextBackgroundEntry = Entry(self.editTextWindow, font=('Arial', 10, 'bold'), width=25, bg='white')
        self.changeTextBackgroundEntry.place(x=5, y=155)
        self.changeTextBackgroundButton = Button(self.editTextWindow, text='Change Text \nBackground Colour', font=('Ariel', 10),command=lambda: self.changeTXTBGColourFunc(self.changeTextBackgroundEntry.get()))
        self.changeTextBackgroundButton.place(x=195, y=145, height=40, width=130)

        self.changeTextLabel = Label(self.editTextWindow, text="Enter colour to change the text:", fg="white",font=('Arial', 10, 'bold'), bg="black", width=30)
        self.changeTextLabel.place(x=-17, y=200)
        self.changeTextEntry = Entry(self.editTextWindow, font=('Arial', 10, 'bold'), width=25, bg='white')
        self.changeTextEntry.place(x=5, y=235)
        self.changeTextButton = Button(self.editTextWindow, text='Change Text \nColour', font=('Ariel', 10),command=lambda: self.changeTXTFGColourFunc(self.changeTextEntry.get()))
        self.changeTextButton.place(x=195, y=225, height=40, width=130)
    '''If the user clicks the "changeBackgroundButton" this function will take what the user inputted add it to the command
    and send it to the server'''
    def changeBGColourFunc(self, colour):
        changeBGColCommand = 'new/bg/col' + '+' + colour
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(changeBGColCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))
    '''If the user clicks the "changeTextBackgroundButton" this function will take what the user inputted add it to the command
    and send it to the server'''
    def changeTXTFGColourFunc(self, colour):
        changeTXTBGColCommand = 'new/txtfg/col' + '+' + colour
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(changeTXTBGColCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))
    '''If the user clicks the "changeTextButton" this function will take what the user inputted add it to the command
    and send it to the server'''
    def changeTXTBGColourFunc(self, colour):
        changeTXTBGColCommand = 'new/txtbg/col' + '+' + colour
        readyEncryptedCommand = encryption.clientEncryption.encryptMessage(changeTXTBGColCommand)
        client.send(readyEncryptedCommand.encode('utf-8'))

    '''This function is linked to the "sendMessageButton" in the main room it takes the message/command inputted by the
     user and creates a thread and send it to the send message function'''
    def sendButton(self, userMessage):
        self.textCons.config(state=DISABLED)
        self.MessagefromUser = userMessage
        self.entryMsg.delete(0, END)
        startT = threading.Thread(target=self.sendMessage)
        startT.start()


    '''This function takes the message inputted by the send button formats it in the (username) : (message) and encrypts
    the message and sends it'''
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.username}: {self.MessagefromUser}")
            encryptedMessage = encryption.clientEncryption.encryptMessage(message)
            client.send(encryptedMessage.encode('utf-8'))
            break

'''after all the port and host addresses are set above and all the fucntions are declared this calls the first function
to start the client'''
start = chatroom()