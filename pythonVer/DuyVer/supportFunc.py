import os
from socket import *

def getNameFile(fromWhere):
    if fromWhere == "server":
        directName = "./fileOnServer"
    elif fromWhere =="client":
        directName = "."
    result=""
    for _, _, files in os.walk(directName):
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

def padStringLen(string, size):
    tempString = str(len(string))
    while (len(tempString) < size):
        tempString+=" "
    return tempString

def padString(string, size):
    tempString = string
    while (len(tempString) < size):
        tempString+=" "
    return tempString


def processNPrintNameFile(namesFile):
    files = namesFile.split(",")
    print("Files On Server Are:")
    for file in files:
        print("                     "+file)

def checkFileExist(fileName, fromWhere):
    if fromWhere == "server":
            directName = "./fileOnServer"
    elif fromWhere =="client":
        directName = "."
    for _, _, files in os.walk(directName):
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

def downloadFile(conn, fileName, size, fromWhere):
    if fromWhere == "server":
        directName = "DLFromServer/"
    elif fromWhere =="client":
        directName = "fileOnServer/"
    if not os.path.exists(directName):
        os.mkdir(directName)
    tempBuf = 0
    data = 0
    print("Downloading...")
    with open(directName+fileName, "wb") as f:
        while tempBuf < size:
            data=conn.recv(1024)
            tempBuf+=len(data)
            if not data:
                break
            f.write(data)
        if tempBuf == size:
            print("Download Completed")
    f.close()

def padFileNameSize(fileNameSize, size):
    tempString = str(fileNameSize)
    while (len(tempString) < size):
        tempString+=" "
    return tempString

def sendDownloadFile(conn, fileName):
    print("Sending...")
    with open(fileName, 'rb') as f:        
        while True:
            contents = f.read(1024)
            bytesSent=0
            if not contents:
                    break
            while bytesSent < len(contents):
                bytesSent += conn.send(contents)

        f.close()
    print("Send Completed")