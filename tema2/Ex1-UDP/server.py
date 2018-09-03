import socket
from threading import Thread
import logging

from sets import Set

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

# listen for incoming data and add to sliding window
def listen():
    global currentValue
    while True:
        try:
            dataAddressPair = UDPServer.recvfrom(datasize)
        except:
            break
        databytes = dataAddressPair[0]
        clientAddress = dataAddressPair[1]
        logging.info('Received ' + str(databytes) + ' from ' + str(clientAddress))

        if databytes:
            value = int(databytes)
             
            if value < currentValue + slidingWindowSize:
                #data received
                UDPServer.sendto(databytes, clientAddress)
                logging.info('Send confirmation for ' + str(value))
                #check if number fits current window
                if value >= currentValue and value not in receivedValues:
                    receivedValues.add(value)

            if value > lim:
                break

# process data and remove from sliding window
def process():
    global currentValue
    while True:
        while currentValue in receivedValues:
            receivedValues.remove(currentValue)
            currentValue = currentValue + 1
        if currentValue >= lim:
            break


# create datagram socket on port 5555
UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = '172.111.0.14'; #rt3 ipv4 address
port = 5555
serverAddress = (address, port)
UDPServer.bind(serverAddress);
logging.info('UDP server is started on ' + str(address) + 'address and ' + str(port) + ' port')

# sets constats
currentValue = 1;
lim = 10000;
slidingWindowSize = 20;
datasize = 2048;

# init window
window = []
receivedValues = Set()


listening_thread = Thread(target=listen)
processing_thread = Thread(target=process)

listening_thread.start()
processing_thread.start()

