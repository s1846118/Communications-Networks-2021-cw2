import socket
import sys 
import os
import math
from time import perf_counter

def throughput(time_start, time_end, a_byte_array, payload):
    return (len(a_byte_array)/payload)/(time_end - time_start)

# This is the sending stuff
UDP_IP = sys.argv[1]  # <remote_host> 
UDP_PORT = int(sys.argv[2]) # <port>
fileToSend = sys.argv[3] # <filename>
retryTimeout = int(sys.argv[4]) # Time in miliseconds to resend packet. 
sock = socket.socket(socket.AF_INET, # Internet (Indication of IPv4)
                     socket.SOCK_DGRAM) # UDP
sock.settimeout(0.01)

with open(fileToSend, 'rb') as f: # Open the file to convert to binary
    fr = f.read()
    byteArray = bytearray(fr) # Creates bytearray

# Number of full (1024 byte payload) packets and size of final packet. 
fullPkts = math.floor(len(byteArray)/1024)
finalPkt = len(byteArray) % 1024
byteEnd = 1024
byteStart = 0
seqNumBase10 = 0
EOF = 0
ACK_list = []
if(finalPkt == 0):
    fin = 0
else:
    fin = 1
terminate = 0 
numPks = fullPkts + fin

time_start = perf_counter()
for x in range(fullPkts + fin):
    pkt = bytearray(seqNumBase10.to_bytes(2, byteorder='big'))
    if(finalPkt != 0 and x == fullPkts): # Final packet so EOF set to 1. This only executes if we have over flow. 
        EOF = 1
        pkt.append(EOF) # Full header created
        pkt.extend(byteArray[byteStart:(byteStart+finalPkt)]) # Add payload
    else:
        pkt.append(EOF) # Full header created   
        pkt.extend(byteArray[byteStart:byteEnd]) # Add payload    
    sock.sendto(pkt, (UDP_IP, UDP_PORT)) # Send packet to receiver
    while True: # Here we have for loop true while waiting for ACK (set to false or something when timer runs out)
        try:
            data, addr = sock.recvfrom(3) # Wait for ACK

            curr_Ack = int.from_bytes(data, 'big')
            if not(curr_Ack in ACK_list): # If the ACK isn't yet accounted for we append and move on
                ACK_list.append(curr_Ack)           
                break
            # Our problem here before was that we were running lines 64-67 when our ack WAS in list. Therefor we missed some stuff
            if curr_Ack == numPks - 1:
                break
        except socket.timeout: # If we timeout this happens
            if(EOF == 1 and (curr_Ack == numPks - 1)):
                #print('Retransmit')
                break
            sock.sendto(pkt, (UDP_IP, UDP_PORT)) # Send packet to receiver again as ACK was not received 
    byteStart += 1024
    byteEnd += 1024
    seqNumBase10 += 1

time_end = perf_counter()

x = throughput(time_start, time_end, byteArray, 1024)

print(x)



