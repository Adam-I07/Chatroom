import socket
import threading
import datetime
'''These imports are used once to create the file to save the passwords and usernames'''
import csv
from csv import DictReader
'''from colour import Color - originally installed the library since the uni computer 
dosent have the library installed i just made it into a file called ColourCheck.'''
import ColourCheck

import encryption

'''Assigning the port number and host address. Creating the socket and binding the address to that socket'''
port = 50000
host = '127.0.0.1'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

'''Used to store the client address and usernames of people in the room'''
clients = []
usernames = []


'''Code to create the csv file to store the log in details'''
# with open('loginDetails.csv', 'w', newline='') as file:
#  fieldnames = ['Username', 'Password']
#  writeInCSV = csv.DictWriter(file, fieldnames=fieldnames)
#  writeInCSV.writeheader()

'''When you start the server this is th first function called. The server listens for connections, once it recieves one 
it will bind them together ask for a username, if it recieves a username it will add it to the username list and start
a thread for that client and target the handle function'''
def startProgram():
    print("server is running on " + host)
    server.listen()

    while True:
        client, addr = server.accept()
        startCommand = 'SendUsername'
        sendStartCommandEncrypted = encryption.serverEncryption.encryptMessage(startCommand)
        client.send(sendStartCommandEncrypted.encode('utf-8'))

        recievedMessage = client.recv(1024).decode('utf-8')
        decryptedMessage = encryption.serverEncryption.decryptMessage(recievedMessage)

        usernames.append(decryptedMessage)
        clients.append(client)

        print(f"Current active users are :{usernames}")
        sendToChat(f"{decryptedMessage} has joined the chat!")
        sendToChat(f"{usernames} is currently in the chatroom.")
        global threads
        threads = threading.Thread(target=handleClient, args=(client, addr), daemon=True)
        threads.start()


'''Once the clients thread has started they are put into this loop where they send a message/command to the server
if the command is correct the server will respond an encrypted reply accordingly.'''
def handleClient(client, addr):
    print(f"new connection {addr}")
    while True:
        recievedMessage = client.recv(1024).decode('utf-8')
        decryptedMessage = encryption.serverEncryption.decryptMessage(recievedMessage)
        try:
            '''If the user leaves this removes all the clients information and sends them a command to leave'''
            if '/user|leave/room' in decryptedMessage:
                    index = clients.index(client)
                    userName = usernames[index]
                    sendToChat(f'{userName} has left the chat!')
                    print(f'{userName} has left the chat!')
                    closeCommand = '/user|close|command'
                    encryptCloseComamnd = encryption.serverEncryption.encryptMessage(closeCommand)
                    client.send(encryptCloseComamnd.encode('utf-8'))
                    usernames.remove(userName)
                    clients.remove(client)

            #This command when triggered sends the client all the information of whos in the chatroom
            elif '/users|Show/online/users' in decryptedMessage:
                currentUsersOnline = dict.fromkeys(usernames,"Online")
                currentOnlineUsers = ', '.join([onlineUsers for onlineUsers in sorted(currentUsersOnline.keys())])
                sendToChat("Current users in the chatroom are: {}".format(currentOnlineUsers))
            # This command when triggered sends the client the current date and time
            elif '/users|Show/current/date/time' in decryptedMessage:
                now = datetime.datetime.now()
                sendToChat(now.strftime("The current date is: %d-%m-%y and time is: %H:%M"))
            #The colour function have validation set to them to make sure the client sends an actual colour
            #if not they will get a message back letting them know its not a colour
            elif 'new/txtbg/col' in decryptedMessage:
                col = decryptedMessage.split('+')[1]
                try:
                    ColourCheck.Color(col)
                    txtBGColCommand = ('new/txtbg/col/accepted' + '+' + col)
                    encryptedTXTBGCommand = encryption.serverEncryption.encryptMessage(txtBGColCommand)
                    client.send(encryptedTXTBGCommand.encode('utf-8'))
                except:
                    deniedCommandTXTBG =  ('new/col/declined')
                    deniedCommandEncryptedTXTBG = encryption.serverEncryption.encryptMessage(deniedCommandTXTBG)
                    client.send(deniedCommandEncryptedTXTBG.encode('utf-8'))

            elif 'new/txtfg/col' in decryptedMessage:
                col = decryptedMessage.split('+')[1]
                try:
                    ColourCheck.Color(col)
                    txtFGColCommand = ('new/txtfg/col/accepted' + '+' + col)
                    encryptedTXTFGCommand = encryption.serverEncryption.encryptMessage(txtFGColCommand)
                    client.send(encryptedTXTFGCommand.encode('utf-8'))
                except:
                    deniedCommandTXTFG= ('new/col/declined')
                    deniedCommandEncryptedTXTFG = encryption.serverEncryption.encryptMessage(deniedCommandTXTFG)
                    client.send(deniedCommandEncryptedTXTFG.encode('utf-8'))
            elif 'new/bg/col' in decryptedMessage:
                col = decryptedMessage.split('+')[1]
                try:
                    ColourCheck.Color(col)
                    bgColCommand = ('new/bg/col/accepted' + '+' + col)
                    encryptedBGCommand = encryption.serverEncryption.encryptMessage(bgColCommand)
                    client.send(encryptedBGCommand.encode('utf-8'))
                except:
                    deniedCommandBG = ('new/col/declined')
                    deniedCommandEncryptedBG = encryption.serverEncryption.encryptMessage(deniedCommandBG)
                    client.send(deniedCommandEncryptedBG.encode('utf-8'))
            else:
                #If no commands are specifically triggered the chatroom will print the message for everyone to see
                sendToChat((decryptedMessage))
        #if an error occurs during the loop the program will close that client so the other can carry on
        except:
            print("User left the chat")
            client.close()

'''This is the function that will send back answers from the server to the client'''
def sendToChat(message):
    for client in clients:
        '''each message is encrypted before sending'''
        encryptMessage = encryption.serverEncryption.encryptMessage(message)
        client.send(encryptMessage.encode('utf-8'))

'''after all the port and host addresses are set above and all the fucntions are declared this calls the first function
to start the server'''
startProgram()