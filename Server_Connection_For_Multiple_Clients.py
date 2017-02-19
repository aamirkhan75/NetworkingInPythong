#!/usr/bin/env python
''' This program will connect to client server. 
	Client will create a request format and server 
	will response to Client request with customize information. 
'''
import socket
import time
import datetime
import random
from thread import start_new_thread
import struct

## Network Parameters ## 
ServerIPAddress = '127.0.0.1'
ServerPORT = 10280
ServerSocketNumber = 1206
BUFFER_SIZE = 0x0090

#parsing cleint List to generate server response

def genRSP(parsedREQ,ResponseId):
    ## TO DO
    MessageType = "RSP"
    msTimeStamp =  str(int(round(time.time() * 1000))) # milisecond time stamp value from timer running on client; max length 10
    msTimeStamp = msTimeStamp[:-3]
    RequestID = parsedREQ[2]
    StudentName = parsedREQ[3]
    StudentID = parsedREQ[4]
    ResponseDelay = parsedREQ[5]
    ForeignHostIPAddress = parsedREQ[6]
    ForeignHostServicePort = parsedREQ[7]
    intdelay = int(ResponseDelay)
    ResponeseType = ''
    if(intdelay >= 0  and intdelay < 3000):
        ResponeseType = "1"
    elif (intdelay >= 3000 and intdelay < 4000):
        ResponeseType = "2"
    elif (intdelay == 4000 ):
        ResponeseType = "3"  
    else:
        ResponeseType = "4"          
    MESSAGE = MessageType + "|" + msTimeStamp + "|" + RequestID + "|" + StudentName + "|" + StudentID + "|" + ResponseDelay + "|" + ForeignHostIPAddress + "|" + ForeignHostServicePort + "|"  + str(ServerSocketNumber)+ "|" + ServerIPAddress + "|" + str (ServerPORT) + "|" + ResponseId + "|" + ResponeseType + "|" 
    TCPHeader =  struct.pack ('>H',(len(MESSAGE))) # compute length of message (first byte will always be 00
    MESSAGE = TCPHeader + MESSAGE
    print "sent data:", MESSAGE 
    return MESSAGE

def parseREQ(REQ):
    return REQ.split('|')
    
def trailerRecord():
    Mydate = time.strftime("%m%d%y")
    MyTime = time.strftime("%H%M%S")
    ## TO DO


def GenShutDown():
    MessageType = "FIN" 
    MESSAGE = MessageType 
    TCPHeader =  struct.pack ('>H',(len(MESSAGE))) # compute length of message (first byte will always be 00
    MESSAGE = TCPHeader + MESSAGE
    print "sent data:", MESSAGE
    return MESSAGE

# thread for each individual client that connects to the server
def client_thread(conn, addr):
    fn = 'Lab4.Scenario2.KhanA.txt'
    
    fn += '.txt'
    f = open(fn, 'a') # log file per client
    while 1:
        REQ = conn.recv(BUFFER_SIZE) # get REQ
        if not REQ: break
        print "received:", REQ
        f.write(REQ + '\n')
        ResponseId =str(random.randrange(1, 25000)) 
        parsedREQ = parseREQ(REQ) # parse request for things the server needs for response
        RES = genRSP(parsedREQ,ResponseId) # generate a response for the client using the parsed request
        f.write(RES + '\n')
        print "sent:", RES
        conn.send(RES)  # echo
    #f.write(trailerRecord()) # TODO: append trailer info to log file
    f.close()
    conn.close()

    
def main():

    ## Set up Server ##
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ServerIPAddress, ServerPORT))
    s.listen(2)
    ##
    
    ## Listener loop to establish connection with a client  ##
    while True:
        conn, addr = s.accept()
        print("Client connected: " + addr[0] + ":" + str(addr[1]))

        start_new_thread(client_thread, (conn,addr[0])) # starts new thread when client arrives
    ##
    print ("main: closing...")
    s.close()
    f.close()




if __name__ == "__main__":
    main()