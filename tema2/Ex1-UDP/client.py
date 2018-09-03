import logging
import socket
from threading import Thread
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

# send data
def send():
    global currentValue
    while True:
        offset = currentValue
        newValueLim = min(offset + slidingWindowSize, lim + 1)
        if offset > lim:
            UDPClient.close()
            break

        for newValue in range(offset, newValueLim):
            if newValue in receivedValues:
                continue
            logging.info('Send ' + str(newValue))
            time.sleep(timeout)
            UDPClient.sendto(str(newValue), serverAddress)


# listen for incoming data (ack) 
def listen():
    global currentValue
    while True:
        try:
            dataAddressPair = UDPClient.recvfrom(datasize)
        except:
            break
        databytes = dataAddressPair[0]
        serverAddress = dataAddressPair[1]
        logging.info('Received ' + str(databytes) + ' from ' + str(serverAddress))

        if databytes:
            value = int(databytes)
             
            #check if number fits current window
            if currentValue <= value and value < currentValue + slidingWindowSize:
                if value not in values_received:
                    receivedValues.add(value)


# process data and remove from sliding window
def process():
    global currentValue
    while True:
        while currentValue in receivedValues:
            receivedValues.remove(currentValue)
            currentValue = currentValue + 1

# create client and start threads for sending, listening and processing data
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = '172.111.0.14'; #rt3 ipv4 address
port = 5555
serverAddress = (address, port)

# sets constats
currentValue = 1;
lim = 10000;
slidingWindowSize = 20;
datasize = 2048;
timeout = 0.1

# init window
window = []
receivedValues = set()

listening_thread = Thread(target=listen)
sending_thread = Thread(target=send)
processing_thread = Thread(target=process)

sending_thread.start()
listening_thread.start()
processing_thread.start()

