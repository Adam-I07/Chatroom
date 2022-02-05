
class DiffieHellmanEncryption(object):
    def __init__(self, serverPublicKey, clientPublicKey, privateKey):
        self.serverPublicKey = serverPublicKey
        self.clientPublicKey = clientPublicKey
        self.privateKey = privateKey
        self.fullKey = None

    '''going to get a partial key using the serverPublic key as as the base
    and the client public key as the modulo'''
    def createPartialKey(self):
        finalPartialKey = self.serverPublicKey ** self.privateKey
        finalPartialKey = finalPartialKey % self.clientPublicKey
        return finalPartialKey

    '''This time we are going to do the same calculations as the partial key but 
    rather than using your own key you are going to use the other recievers key 
    to generate a common encryption key'''
    def createFullKey(self, partial_key_r):
        newFullKey = partial_key_r ** self.privateKey
        finalFullKey = newFullKey % self.clientPublicKey
        self.fullKey = finalFullKey
        return finalFullKey

    '''To encrypt the message the program will get the message and 
    use the key to work out a integer value to add the key to it for the current character in the 
    message after the key is added to the character it is converted back to a character and stored in
    the original charatcers place.'''
    def encryptMessage(self, message):
        encryptedMessage = ""
        key = self.fullKey
        for i in message:
            encryptedMessage += chr(ord(i) + key)
        return encryptedMessage

    '''the decryption method recieves the encrypted message. It will basically do the inverse
        of the encryption method. The method will store the encrypted messsage then take a character at a time
        convert it into its integer and this time will minus the key to get the original value and store it. Will
        do this to the whole message untill it is fully decrypted'''
    def decryptMessage(self, encryptedMessage):
        decryptedMessage = ""
        key = self.fullKey
        for i in encryptedMessage:
            decryptedMessage += chr(ord(i) - key)
        return decryptedMessage

#Assigning public and private keys to the server and client
serverPublicKey = 123
serverPrivateKey = 252
clientPublicKey = 667
clientPrivateKey = 999

#assigning key values to the server and client ready to be used in the class to create the final keys for encryption
serverEncryption = DiffieHellmanEncryption(serverPublicKey, clientPublicKey, serverPrivateKey)
clientEncryption = DiffieHellmanEncryption(serverPublicKey, clientPublicKey, clientPrivateKey)

'''assigns the server and client each others keys so they can generate the same key.'''
serverPartialKey = serverEncryption.createPartialKey()
clientPartialKey = clientEncryption.createPartialKey()
'''gives the server and client each others partial key to send messages'''
serverFullKey = serverEncryption.createFullKey(clientPartialKey)
clientFullKey = clientEncryption.createFullKey(serverPartialKey)
