"""
This code is for protostar net2 challange.
Will connect to net2 network daemon, read 4 integers reverse byte order, add them up, reverse order total and send back to server.
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
s.settimeout(2) #Raise exception if no data received after 2 seconds, Use this timeout to begin processing data received from server.

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

recv_array = []
total = 0

try:
    #Now receive data
    while True:
        recv = s.recv(4096)
        recv_array.append(recv)
        print "Received: %s" %recv

except socket.timeout:
    print("Timeout. Server has finished sending data. Time to add up all the values.")
    for bytes in recv_array:
        hexval = bytes.encode('hex')
        integer = struct.unpack("<L", bytes)[0] #L=unsigned long 4 bytes, < little endian and unpacked to integer
        total += integer
        print "Received bytes %s converted little endian %s which resulted in an integer %s" %(hexval, hex(integer), integer)
    rev_bytes = struct.pack("<L", total)#reverse bytes received for little endian
    print "Total up the integers %s, reverse byte order from %s to %s and send" %(total, hex(total), rev_bytes.encode('hex'))
    print "Sending challenge to server"
    s.sendall(rev_bytes)

    recv = s.recv(4096)
    print recv
except socket.error:
 #Send failed
    print 'Send failed'
    sys.exit()

print 'Done.'
