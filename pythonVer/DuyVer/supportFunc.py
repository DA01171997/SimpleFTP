import os
from socket import *

def getNameFile():
    result=""
    for _, _, files in os.walk("./fileOnServer"):
        for file in files:
            result += file + ','
    return result

def sendSizeFunc(conn, fileToSend):
    bytesSent=0
    while bytesSent !=40:
        bytesSent += conn.send(fileToSend[bytesSent:].encode())

def sendStringFunc(conn, string):
    bytesSent=0
    while bytesSent !=len(string):
        bytesSent += conn.send(string[bytesSent:].encode())

def recieveStringFunc(conn, size=1040):
    tempBuf =""
    data=""
    while len(data) != size:
        tempBuf = conn.recv(size)
        if not tempBuf:
            break
        else:
            data+= tempBuf.decode()
    return data

def menu():
    ######"What would you like to do?")
    print("                           get - download file")
    print("                           put - upload file")
    print("                           ls - list files")
    print("                           help - print options")
    print("                           quit - terminate program")

def getMenuOption():
    option = input("fpt> ")
    return option

def readLines(conn, recv_buffer = 4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = conn.recv(recv_buffer)
        buffer += data.decode()
        #while buffer.find(delim) != -1:
        #    line, buffer = buffer.split('n',1)
        yield buffer

def padString(string, size):
    tempString = str(len(string))
    while (len(tempString) < size):
        tempString+=" "
    return tempString

def processNPrintNameFile(namesFile):
    files = namesFile.split(",")
    print("Files On Server Are:")
    for file in files:
        print("                     "+file)

def getFilenameFromUser():
        filename = input("What file would you like to get?") 
        return

def checkFileExist(fileName):
    for _, _, files in os.walk("./fileOnServer"):
        for file in files:
            if file == fileName:
                    return True
    return False

def sendACK(conn, typeNum):
    if typeNum ==0:
        type = "Errr"
    elif typeNum ==1:
        type = "Okay"
    elif typeNum ==2:
        type = "Exst"
    elif typeNum ==3:
        type = "NEst"
    elif typeNum ==4:
        type = "Cont"
    elif typeNum ==5:
        type = "NCnt"
    sendStringFunc(conn, type)

def recieveACK(conn):
    ackSize = 4
    ack = recieveStringFunc(conn, ackSize)
    return ack

def continueOption():
    stopOption = False
    while (not stopOption):
        subOption = input("Try again?(Y/N) ")
        if subOption == 'Y' or subOption  == 'y':
            return True
        elif subOption == 'N' or subOption  == 'n':
            return False
        else:
            print("Invalid Option. Please Choose again")
