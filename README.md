SIMPLE FTP
Implemented by: Alex Truong, Astha Sharma, Duy Do
Last Updated: 12/19/2018

Purpose: 
Reliable File Transfer Protocol with server and client application using socket programming. Client can upload(put) and download(get) file from the server. 

*IMPORTANT: This FTP needs to be set up before use.
*IMPORTANT: This version doesn’t encrypt data, use with cautions.

Setup Instructions:
	1.	Both client.py and server.py need it own copy of supportFunc.py.
	2.	Both client.py and server.py takes in two inputs to the script.
	3.	Run the server.py script before the client.py script. 
	4.	client.py  <IP> <PORTNUM>
	5.	server.py <IP> <PORTNUM>
	6.	Setup for client.py
		a.	Place client.py and supportFunc.py in the same parent directory that contains files that you wish to put on server. Any file in the parent directory(.) , same directory where client.py is (./client.py) can be put to server.
		b.	When you get a file from the server, client will create subdirectory under the same parent directory with client.py call DLFromServer/ (./DLFromServer/) if the subdirectory doesn’t already exists, and client will places the get files inside that subdirectory.
	7.	Setup for server.py
		a.	Place client.py and supportFunc.py in the same parent directory. Within that same parent directory create a subdirectory name fileOnServer (./fileOnServer/) and place any file that you want to send to the client inside the fileOnServer/ subdirectory. Any file that is put on the server by the client will also be placed in the fileOnServer/ subdirectory.

User Options:
	1.	get - download file
	2.	put - upload file
	3.	ls - list files
	4.	help - print options
	5.	quit - terminate program
