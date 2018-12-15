import sys
import os
from socket import *
from supportFunc import * 

if regexArgChecks(sys.argv) != True:
    sys.exit(0)

IP_TO_CONNECT = sys.argv[1]
PORT_NUMBER = int(sys.argv[2])

#PORT_NUM = 8080
SERVER_SOCK = socket(AF_INET, SOCK_STREAM)
SERVER_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#SERVER_SOCK.bind(('localhost',PORT_NUM))
SERVER_SOCK.bind((IP_TO_CONNECT, PORT_NUMBER))

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
                print("get") #option received

                #make new FTP connection
                DOWNLOAD_FTP_SOCKET = downloadFTPConnection(IP_TO_CONNECT)

                #get FTP port number
                FTP_PORT = DOWNLOAD_FTP_SOCKET.getsockname()[1]
                FTP_PORT_padded = padString(str(FTP_PORT),40)

                #send FTP port number
                sendStringFunc(SER2CLIENT_CONNECTION, FTP_PORT_padded)
                sendStringFunc(SER2CLIENT_CONNECTION, str(FTP_PORT))

                #set new connection for FTP
                FTP_CONNECTION, newaddr = DOWNLOAD_FTP_SOCKET.accept()
                print('\t\tFTP Connection Established on Port:', FTP_PORT)

                stopGetFlag = False
                while(not stopGetFlag):
                    #receive the fileName size
                    fileNameSize = int(recieveStringFunc(FTP_CONNECTION,40))

                    #receive the fileName
                    fileName = recieveStringFunc(FTP_CONNECTION, fileNameSize)
                    print(fileName)

                    #check if fileName exists
                    print(checkFileExist(fileName,"server"))

                    #if file exist  ACK == Exst  
                    if(checkFileExist(fileName,"server")):
                        #send ACK
                        sendACK(FTP_CONNECTION, 2)

                        #get local file name
                        localFileName = 'fileOnServer/' + fileName

                        #get localFileName size and pad
                        localFileNameSize = os.path.getsize(localFileName)
                        print('local file name size is ', localFileNameSize)
                        localFileNameSizePadded = padFileNameSize(localFileNameSize, 40)

                        #send client the size of file
                        sendStringFunc(FTP_CONNECTION, localFileNameSizePadded)
                                
                        #send file to client
                        sendDownloadFile(FTP_CONNECTION, localFileName)
                        stopGetFlag = True
                        FTP_CONNECTION.close()

                    #if file does not exist  ACK == NEst
                    else:
                        #send ACK
                        sendACK(FTP_CONNECTION, 3)
                        if recieveACK(FTP_CONNECTION) == "NCnt":
                            stopGetFlag = True
                            FTP_CONNECTION.close()

            elif option == "putt":
                print("put") #option received

                #make new FTP connection
                DOWNLOAD_FTP_SOCKET = downloadFTPConnection(IP_TO_CONNECT)

                #get FTP port number
                FTP_PORT = DOWNLOAD_FTP_SOCKET.getsockname()[1]
                FTP_PORT_padded = padString(str(FTP_PORT),40)

                #send FTP port number
                sendStringFunc(SER2CLIENT_CONNECTION, FTP_PORT_padded)
                sendStringFunc(SER2CLIENT_CONNECTION, str(FTP_PORT))

                #set new connection for FTP
                FTP_CONNECTION, newaddr = DOWNLOAD_FTP_SOCKET.accept()
                print('\t\tFTP Connection Established on Port:', FTP_PORT)

                stopPutFlag = False
                while(not stopPutFlag):
                    ack = recieveACK(FTP_CONNECTION)
                    
                    if ack == "Okay":
                        #receive size of file's name, the file's name, and file's size
                        fileNameSize = int(recieveStringFunc(FTP_CONNECTION,40))
                        fileName = recieveStringFunc(FTP_CONNECTION, fileNameSize)
                        fileSize = int(recieveStringFunc(FTP_CONNECTION, 40))

                        #receive the file from client
                        downloadFile(FTP_CONNECTION, fileName, fileSize, "client")

                        #receive file from client complete
                        print('\t\tFile Successfully Retrieved')
                        if recieveACK(FTP_CONNECTION) == "NCnt":
                            stopPutFlag = True
                            FTP_CONNECTION.close()
                            print('\t\tFTP Connection Closed')

                    else:
                        print('\t\tError on Client Side')
                        if recieveACK(FTP_CONNECTION) == "NCnt":
                            stopPutFlag = True
                            FTP_CONNECTION.close()
                            print('\t\tFTP Connection Closed')

            elif option == "lsls":
                print("ls")

                #1 get namesFile
                #2 IMPORTANT NOTE: get namesFile size and pad it to 40 bytes with spaces
                #3 send client the size
                namesFile=getNameFile("server")
                namesFileSizePadded = padString(namesFile,40)
                sendStringFunc(SER2CLIENT_CONNECTION, namesFileSizePadded)
                
                #4 send namesFile
                sendStringFunc(SER2CLIENT_CONNECTION, namesFile)
            
            elif option == "quit":
                print("quit")
                quitFlag = True
    finally:
        print("Close connection")
        SER2CLIENT_CONNECTION.close()
