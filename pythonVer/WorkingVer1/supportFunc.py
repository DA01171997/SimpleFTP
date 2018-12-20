import os
import re
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

def recieveStringFunc(conn, size=40):
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

def regexArgChecks(arguments):
    IP_PATTERN = re.compile("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|localhost)")
    PORT_PATTERN = re.compile("[0-9]{1,5}")
    print(arguments)

    if len(arguments) == 1:
        print('Error -- Must have IP and Port Number Args')
        return False
    elif len(arguments) == 2:
        if bool(IP_PATTERN.match(arguments[1])) != True:
            print('Error:', arguments[1], 'does not match the correct IP format')
        print('Error: Port Number argument not supplied')
        return False
    elif len(arguments) == 3:
        err = 0
        if bool(IP_PATTERN.match(arguments[1])) != True:
            print('Error:', arguments[1], 'does not match the correct IP format')
            err = 1
        if bool(PORT_PATTERN.match(arguments[2])) != True:
            print('Error:', arguments[2], 'does not match the correct Port Number format')
            err = 1
        if err == 1:
            return False
    return True

def downloadFTPConnection(ipAddr):
    #create download FTP connection
    FTP_DL_SOCK = socket(AF_INET, SOCK_STREAM)
    FTP_DL_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    FTP_DL_SOCK.bind((ipAddr, 0))
    FTP_DL_SOCK.listen(1)
    return FTP_DL_SOCK

def uploadFTPConnection(ipAddr, PORT_NUM):
    #create upload FTP connection
    FTP_UL_SOCK = socket(AF_INET, SOCK_STREAM)
    FTP_UL_SOCK.connect((ipAddr, PORT_NUM))
    return FTP_UL_SOCK
