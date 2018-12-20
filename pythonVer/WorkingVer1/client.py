import sys
from socket import *
from supportFunc import *

#check to see if cmd line args are correct
if regexArgChecks(sys.argv) != True:
    sys.exit(0)

IP_TO_CONNECT = sys.argv[1]
PORT_NUMBER = int(sys.argv[2])

#PORT_NUM = 8080
CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect((IP_TO_CONNECT, PORT_NUMBER))
#CLIENT_SOCK.connect(('localhost', PORT_NUM))
print("Client Connecting...")

#let server know client is connected
#this message will be 26 bytes
connectMessage="Client Connected to Server"
sendStringFunc(CLIENT_SOCK,connectMessage)

#get menu option
#IMPORTANT NOTE: all option are padded to be 4 bytes
quitFlag = False
print("What would you like to do?")
menu()
while(not quitFlag):
    option = getMenuOption()

    if option == "get":
        option="gett"
        
        #send option put to server
        sendStringFunc(CLIENT_SOCK,option)

        #receive port number size from server
        FTP_PORT_size = int(recieveStringFunc(CLIENT_SOCK, 40))

        #receive port number from server
        FTP_PORT = int(recieveStringFunc(CLIENT_SOCK, FTP_PORT_size))

        #set new connection for FTP
        UPLOAD_FTP_SOCKET = uploadFTPConnection(IP_TO_CONNECT, FTP_PORT)
        print('FTP Connection Established on Port:', FTP_PORT)

        stopGetFlag = False
        while(not stopGetFlag):
            #get what file user wants to send
            fileName = input("What file would you like to receive? ")

            #send server size of fileName
            fileNameSizePadded = padString(fileName,40)
            sendStringFunc(UPLOAD_FTP_SOCKET,fileNameSizePadded)

            #send server the fileName
            sendStringFunc(UPLOAD_FTP_SOCKET, fileName)

            #check ACK
            ack = recieveACK(UPLOAD_FTP_SOCKET)
            if ack=="Exst":

                #get size of file from server
                downloadFileSize = int(recieveStringFunc(UPLOAD_FTP_SOCKET, 40))
                print('downloadFileSize is', downloadFileSize)

                #download file from server
                downloadFile(UPLOAD_FTP_SOCKET, fileName, downloadFileSize, "server")

                UPLOAD_FTP_SOCKET.close()
                stopGetFlag = True
            else:
                print("File doesn't exist")
                #continue get or quit?
                if(not continueOption()):
                    stopGetFlag = True
                    sendACK(UPLOAD_FTP_SOCKET,5)
                    UPLOAD_FTP_SOCKET.close()
                else:
                    sendACK(UPLOAD_FTP_SOCKET,1)
     
    elif option == "put":
        option="putt"

        #send option put to server
        sendStringFunc(CLIENT_SOCK,option)

        #receive port number size from server
        FTP_PORT_size = int(recieveStringFunc(CLIENT_SOCK, 40))

        #receive port number from server
        FTP_PORT = int(recieveStringFunc(CLIENT_SOCK, FTP_PORT_size))

        #set new connection for FTP
        UPLOAD_FTP_SOCKET = uploadFTPConnection(IP_TO_CONNECT, FTP_PORT)
        print('FTP Connection Established on Port:', FTP_PORT)

        stopPutFlag = False
        fileExists = False
        while(not stopPutFlag):
            #input name of file to upload
            fileName = input("File to upload: ")

            if checkFileExist(fileName, "client"):
                #send Okay to server to be ready to send file
                sendACK(UPLOAD_FTP_SOCKET, 1)

                #get size of file's name, the file's name, and file's size
                fileNameSizePadded = padString(fileName, 40)
                localFileNameSize = os.path.getsize(fileName)
                localFileNameSizePadded = padFileNameSize(localFileNameSize, 40)

                #send size of file's name, the file's name, and file's size
                sendStringFunc(UPLOAD_FTP_SOCKET, fileNameSizePadded)
                sendStringFunc(UPLOAD_FTP_SOCKET, fileName)
                sendStringFunc(UPLOAD_FTP_SOCKET, localFileNameSizePadded)

                #upload the file to server
                sendDownloadFile(UPLOAD_FTP_SOCKET, fileName)

                #upload of file to server complete
                print('Successfully Uploaded')
                if not continueOption():
                    stopPutFlag = True
                    sendACK(UPLOAD_FTP_SOCKET, 5)
                    UPLOAD_FTP_SOCKET.close()
                    print('FTP Connection Closed')
                else:
                    sendACK(UPLOAD_FTP_SOCKET, 4)

            else:
                sendACK(UPLOAD_FTP_SOCKET, 0)
                print('Cannot Upload -- File Does Not Exist')
                
                if not continueOption():
                    stopPutFlag = True
                    sendACK(UPLOAD_FTP_SOCKET, 5)
                    UPLOAD_FTP_SOCKET.close()
                    print('FTP Connection Closed')
                else:
                    sendACK(UPLOAD_FTP_SOCKET, 4)
                
    elif option == "ls":
        option="lsls"
        sendStringFunc(CLIENT_SOCK,option)

        #receive the namesFile size
        namesFileSize = int(recieveStringFunc(CLIENT_SOCK, 40))

        #receive the namesFile
        #process the nameFile string and print
        namesFile = recieveStringFunc(CLIENT_SOCK, namesFileSize) 
        processNPrintNameFile(namesFile)
        
    elif option == "quit":
        sendStringFunc(CLIENT_SOCK,option)
        quitFlag = True
    elif option == "help":
        print("What would you like to do?")
        menu()
    else:
        print("Invalid Option. Please Choose again")

CLIENT_SOCK.close()
