import sys
import os
from socket import *
from supportFunc import * 

PORT_NUM = 8080
SERVER_SOCK= socket(AF_INET, SOCK_STREAM)
SERVER_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER_SOCK.bind(('localhost',PORT_NUM))
SERVER_SOCK.listen(1)
print("Server Now Listening...")
while 1:
    SER2CLIENT_CONNECTION, addr = SERVER_SOCK.accept()
    try:
        #check to make sure client is connected
        #this message will be 26 bytes
        connectedMessage = recieveStringFunc(SER2CLIENT_CONNECTION,26)
        print(connectedMessage)
        #get options from client
        #IMPORTANT NOTE: all option are padded to be 4 bytes
        quitFlag = False
        while(not quitFlag):
            option = recieveStringFunc(SER2CLIENT_CONNECTION, 4)
            if option == "gett":
                print("get")
                
                stopGetFlag = False
                while(not stopGetFlag): 
                    #receive the fileName size
                    fileNameSize = int(recieveStringFunc(SER2CLIENT_CONNECTION,40))
                    print(fileNameSize)

                    #receive the fileName
                    fileName = recieveStringFunc(SER2CLIENT_CONNECTION, fileNameSize)
                    print(fileName)


                    #check if fileName exists
                    print(checkFileExist(fileName))

                    #send ACK   
                    if(checkFileExist(fileName)):
                        sendACK(SER2CLIENT_CONNECTION, 2)
                        stopGetFlag = True
                    else:
                        sendACK(SER2CLIENT_CONNECTION, 3)
                        if recieveACK(SER2CLIENT_CONNECTION) == "NCnt":
                            stopGetFlag = True


            elif option == "putt":
                print("put")
            elif option == "lsls":
                print("ls")

                #1 get namesFile
                #2 IMPORTANT NOTE: get namesFile size and pad it to 40 bytes with spaces
                #3 send client the size
                namesFile=getNameFile()
                namesFileSizePadded = padString(namesFile,40)
                sendStringFunc(SER2CLIENT_CONNECTION, namesFileSizePadded)
                print("      sent nameFilesSize")
                #4 send namesFile
                print("      sent nameFiles")
                sendStringFunc(SER2CLIENT_CONNECTION, namesFile)
            elif option == "quit":
                print("quit")
                quitFlag = True
    finally:
        print("Close connection")
        SER2CLIENT_CONNECTION.close()

