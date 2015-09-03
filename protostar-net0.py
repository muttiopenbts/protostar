"""
This code is for protostar net0 challange.
Will connect to net0 network daemon, read the decimal value send from server, convert to hex, then send back in little endian.
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
    print recv
    m = re.search('\'(.+?)\'', recv) #search for decimal value between single quotes
    if m:
        found = m.group(1)

    #Set the whole string
    hexval = hex(int(found))
    hexval = hexval[2:]#remove leading '0x' characters
    rev_bytes = struct.pack('<L',int(found))#Convert big endian to little
    print "challenge, %s send back hex %s in little endian %s" %(found,hexval,rev_bytes.encode('hex'))
    s.sendall(rev_bytes)

    recv = s.recv(4096)
    print recv
except socket.error:
 #Send failed
    print 'Send failed'
    sys.exit()

print 'Done.'
