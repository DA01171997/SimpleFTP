from socket import *
from supportFunc import *

PORT_NUM = 8080
CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(('localhost', PORT_NUM))
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
            fileName = input("What file would you like to send? ")

            #send server size of fileName
            fileNameSizePadded = padString(fileName,40)
            sendStringFunc(CLIENT_SOCK,fileNameSizePadded)

            #send server the fileName
            sendStringFunc(CLIENT_SOCK, fileName)

            #check ACK
            ack = recieveACK(CLIENT_SOCK)
            print(ack)
            if ack=="Exst":
                stopGetFlag = True
                print("sending file")
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