import socket
import socket
import sys 
import os
import math
from time import perf_counter

# This is the receiving stuff
UDP_IP = "127.0.0.1" # Local host 
UDP_PORT = int(sys.argv[1]) # <port>
filename = sys.argv[2] # <filename>
sock = socket.socket(socket.AF_INET, # Internet (Indication of IPv4)
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) # We have to bind the IP host address to this port because it tells us which port we should send incoming packets too. 

image = bytearray() 
seq_list = []
while True:
    data = None
    data, addr = sock.recvfrom(1027) # buffer size set to 1027
    if not(data == None): # Packet received so we send ACK
        seq = int.from_bytes(data[:2], byteorder='big')
        ACK = (seq).to_bytes(2, byteorder='big')
        sock.sendto(ACK, addr)
        if not(seq in seq_list): # If we have not received a duplicate packet then we add to image, otherwise we pass         
            image.extend(data[3:]) # First three bytes seq number and EOF
            seq_list.append(seq)
    if(data[2] == 1): # EOF flag
        break
        
with open(filename, 'wb') as f:
    f.write(image)
print('Image transfer done!')
print(seq_list)
print(len(seq_list))