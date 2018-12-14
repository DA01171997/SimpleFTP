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

                    #receive the fileName
                    fileName = recieveStringFunc(SER2CLIENT_CONNECTION, fileNameSize)
                    print(fileName)


                    #check if fileName exists
                    print(checkFileExist(fileName,"server"))

                    
                    #if file exist  ACK == Exst  
                    if(checkFileExist(fileName,"server")):
                        #send ACK
                        sendACK(SER2CLIENT_CONNECTION, 2)

                        #get local file name
                        localFileName = './fileOnServer/' + fileName

                        #get localFileName size and pad
                        localFileNameSize = os.path.getsize(localFileName)
                        print('local file name size is ', localFileNameSize)
                        localFileNameSizePadded = padFileNameSize(localFileNameSize, 40)

                        #send client the size of file
                        sendStringFunc(SER2CLIENT_CONNECTION, localFileNameSizePadded)
                                
                        #send file to client
                        sendDownloadFile(SER2CLIENT_CONNECTION, localFileName)
                        stopGetFlag = True
                    #if file does not exist  ACK == NEst
                    else:
                        #send ACK
                        sendACK(SER2CLIENT_CONNECTION, 3)
                        if recieveACK(SER2CLIENT_CONNECTION) == "NCnt":
                            stopGetFlag = True


            elif option == "putt":
                print("put")
                stopPutFlag = False
                putFlag = False
                while( not stopPutFlag):
                    ack = recieveACK(SER2CLIENT_CONNECTION)
                    if ack == "Okay":
                        stopPutFlag = True
                        putFlag = True
                    elif ack == "NCnt":
                        stopPutFlag = True
                print(" put released")
                print(putFlag)

                #if ack for put is good
                if (putFlag):
                    print("File Receiving...")


                    #get file name's size
                    fileNameSizePadd = int(recieveStringFunc(SER2CLIENT_CONNECTION,40))

                    #get name of file from client
                    fileName = recieveStringFunc(SER2CLIENT_CONNECTION,fileNameSizePadd)
                    print(fileName)
                    #get size of file from client
                    downloadFileSize = int(recieveStringFunc(SER2CLIENT_CONNECTION, 40))
                    print('downloadFileSize is', downloadFileSize)

                    #download file from server
                    downloadFile(SER2CLIENT_CONNECTION, fileName, downloadFileSize, "client")

            elif option == "lsls":
                print("ls")

                #1 get namesFile
                #2 IMPORTANT NOTE: get namesFile size and pad it to 40 bytes with spaces
                #3 send client the size
                namesFile=getNameFile("server")
                namesFileSizePadded = padStringLen(namesFile,40)
                sendStringFunc(SER2CLIENT_CONNECTION, namesFileSizePadded)
                
                #4 send namesFile
                sendStringFunc(SER2CLIENT_CONNECTION, namesFile)
            
            elif option == "quit":
                print("quit")
                quitFlag = True
    finally:
        print("Close connection")
        SER2CLIENT_CONNECTION.close()

