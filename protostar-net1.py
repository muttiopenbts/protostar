"""
This code is for protostar net1 challange.
Will connect to net1 network daemon, read the bytes sent from the server, convert to little endian then decimal and send back to server.
"""
import socket
import sys
import re
import struct

try:
 #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'

host = sys.argv[1]
port = sys.argv[2]

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
 #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip

#Connect to remote server
s.connect((remote_ip, int(port)))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

try:
 #Now receive data
    recv = s.recv(4096)
    print "Received: %s" %recv

    #Set the whole string
    hexval = recv.encode('hex')
    rev_bytes = struct.unpack("<L", recv)[0]#reverse bytes received for little endian
    print "challenge, send back hex 0x%s in little endian order %s then decimal %s" %(hexval,hex(rev_bytes),rev_bytes)
    s.sendall(str(rev_bytes)+"\n") 

    recv = s.recv(4096)
    print recv
except socket.error:
 #Send failed
    print 'Send failed'
    sys.exit()

print 'Done.'
