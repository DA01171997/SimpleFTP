import sys, re
from socket import *
from supportFunc import *

IP_PATTERN = re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
PORT_PATTERN = re.compile("[0-9]{1,5}")

if len(sys.argv) == 1:
    sys.exit('Error -- Must have IP and Port Number Args')
elif len(sys.argv) == 2:
    if bool(IP_PATTERN.match(sys.argv[1])) != True:
        print('Error:', sys.argv[1], 'does not match the correct IP format')
    print('Error: Port Number argument not supplied')
    sys.exit(0)
elif len(sys.argv) == 3:
    err = 0
    if bool(IP_PATTERN.match(sys.argv[1])) != True:
        print('Error:', sys.argv[1], 'does not match the correct IP format')
        err = 1
    if bool(PORT_PATTERN.match(sys.argv[2])) != True:
        print('Error:', sys.argv[2], 'does not match the correct Port Number format')
        err = 1
    if err == 1:
        sys.exit(0)


IP_TO_CONNECT = sys.argv[1]
PORT_NUMBER = int(sys.argv[2])

PORT_NUM = 8080
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
        sendStringFunc(CLIENT_SOCK,option)
        
        stopGetFlag = False
        while(not stopGetFlag):
            #get what file user wants to send
            fileName = input("What file would you like to receive? ")

            #send server size of fileName
            fileNameSizePadded = padString(fileName,40)
            sendStringFunc(CLIENT_SOCK,fileNameSizePadded)

            #send server the fileName
            sendStringFunc(CLIENT_SOCK, fileName)

            #check ACK
            ack = recieveACK(CLIENT_SOCK)
            if ack=="Exst":

                #get size of file from server
                downloadFileSize = int(recieveStringFunc(CLIENT_SOCK, 40))
                print('downloadFileSize is', downloadFileSize)

                #download file from server
                downloadFile(CLIENT_SOCK, fileName, downloadFileSize, "server")

                stopGetFlag = True
            else:
                print("File doesn't exist")
                #continue get or quit?
                if(not continueOption()):
                    stopGetFlag = True
                    sendACK(CLIENT_SOCK,5)
                else:
                    sendACK(CLIENT_SOCK,1)
     
    elif option == "put":
        option="putt"
        sendStringFunc(CLIENT_SOCK,option)

        stopPutFlag = False
        while(not stopPutFlag):
            #put what file user wants to upload
            fileName = input("What file would you like to upload to server? ")

            #if file exists on client side
            if checkFileExist(fileName,"client"):
                sendACK(CLIENT_SOCK, 1)

                #upload fileName's name size to server
                fileNameSizePadded = padString(fileName,40)
                sendStringFunc(CLIENT_SOCK,fileNameSizePadded)

                #upload fileName's name to server
                sendStringFunc(CLIENT_SOCK, fileName)

                #get localFileName size and pad from client side
                localFileNameSize = os.path.getsize(fileName)
                localFileNameSizePadded = padFileNameSize(localFileNameSize, 40)

                #upload the size of file to server
                sendStringFunc(CLIENT_SOCK, localFileNameSizePadded)

                #upload file to server
                sendDownloadFile(CLIENT_SOCK, fileName)
                stopPutFlag = True
            else:
                print("File cannot be uploaded -- does not exist")
                sendACK(CLIENT_SOCK, 0)
                #continue put or quit
                if(not continueOption()):
                    stopPutFlag = True
                    sendACK(CLIENT_SOCK,5)
                else:
                    sendACK(CLIENT_SOCK,1)

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
