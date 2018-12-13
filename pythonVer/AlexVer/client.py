from socket import *
from time import sleep

IP_ADDR = '192.168.0.31'
PORT_NUMBER = 8080
SERVER_ADDR = (IP_ADDR, PORT_NUMBER)

def send_buffer_size(conn, bufferSize):
    try:
        conn.send(bufferSize.encode())
        print('Successfully sent buffer size of', bufferSize, 'to', IP_ADDR)
    except:
        print('ERROR: Buffer size cannot be sent to server')
    finally:
        print()

def send_message(conn, message, bufferSize):
    try:
        conn.send(message.encode())
        print('Successfully sent message \'' + message + '\' to server')
    except:
        print('ERROR: Message cannot be sent or cannot receive response from server')
    finally:
        response = print_response_from_server(conn, bufferSize)
        print(response)

def get_buffer_size_from_server(conn):
    try:
        response = conn.recv(1024)
        print(response)
        response = int(response.decode())
    except:
        print('ERROR: Could not receive a response from the server')
    finally:
        print()
    return response

def print_response_from_server(conn, bufferSize):
    try:
        response = ""
        while len(response) != bufferSize:
            tmpBuff = conn.recv(bufferSize)
            if not tmpBuff:
                break
            response += tmpBuff.decode()
    except:
        print('ERROR: Could not receive a response from the server')
    finally:
        print()
    return response




###### USE THIS HERE DUY ######
def get_file_from_server(fileName, conn, bufferSize):
    try:
        response = ""
        with open(fileName, "w") as f:
            while len(response) != bufferSize:
                newBuff = conn.recv(bufferSize)
                if not newBuff:
                    break
                response += newBuff.decode()
                f.write(response)
            f.close()
    except:
        print('ERROR')
    finally:
        print()
    return response
################################





def main():
    conn = socket(AF_INET, SOCK_STREAM)
#    conn.connect((IP_ADDR, PORT_NUMBER))
    conn.connect(('localhost', PORT_NUMBER))

    print('\n--------------------')
    print('\nConnected to server at:\nIP Address:', IP_ADDR, '\nPort Number:', PORT_NUMBER, '\n')
    print('--------------------')

    bufferSize = get_buffer_size_from_server(conn) #1

    print('Files on server:')
    response = print_response_from_server(conn, bufferSize) #2
    print(response)

    answer = input('Enter name of file to download: ') #3
    print('\n--------------------\n')
    bufferSize = len(answer)   

    send_buffer_size(conn, str(bufferSize)) #3

    send_message(conn, answer, bufferSize)

    fileSize = get_buffer_size_from_server(conn) # get the file size
    print(fileSize)

    response = get_file_from_server(answer, conn, fileSize) # write to file until filesize is met
    print(response)

    conn.close()

if __name__ == "__main__":
    main()