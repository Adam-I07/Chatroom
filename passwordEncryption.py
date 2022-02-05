#This is ceasar cipher used to store the passwords.

'''The encrypt takes the original message and findes the index of each letter in the values string and
adds 5 to it to get the new value and stores it in the encryptedMessage. Once its done that for all of the
letters in the message it returns the new encrypted message.'''
def encrypt(message):
    encryptedMessage = ""
    for i in message:
        if i in values:
            letterIndex = (values.find(i) + key) % len(values)
            encryptedMessage = encryptedMessage + values[letterIndex]
        else:
            encryptedMessage = encryptedMessage + i
    return encryptedMessage

'''The decrypt takes the decrpted message and findes the index of each letter in the values string and takes
away 5 from it to get the value and stores it in the decryptedMessage. Once its done that for all of the
letters in the message it returns the message.'''
def decrypt(message):
    decrptedMessage = ""
    for i in message:
        if i in values:
            letterIndex = (values.find(i) - key) % len(values)
            decrptedMessage = decrptedMessage + values[letterIndex]
        else:
            decrptedMessage = decrptedMessage + i
    return decrptedMessage

key = 5
values = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"