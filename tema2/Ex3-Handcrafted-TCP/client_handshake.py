# inainte de toate trebuie adaugata o regula de ignorare 
# a pachetelor RST pe care ni le livreaza kernelul automat
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
from scapy.all import *
import socket
import logging
import time


logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

ip = IP()
ip.src = '198.13.0.15'
ip.dst = '198.13.0.14'


tcp = TCP()
tcp.sport = 54321
tcp.dport = 10000
TCPOptions[1]['MSS'] = 2
ip.tos = int('011110' + '11', 2) #ECN 11 DSCP AF32


## SYN ##
tcp.seq = 100
tcp.flags = 'S' # flag de SYN
raspuns_syn_ack = sr1(ip/tcp)

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1

tcp.flags = 'A'
ACK = ip / tcp
send(ACK)


# trimitem 3 caractere
for ch in 'XYZ':
    tcp.flags = 'PAEC' # PSH, ACK, ECE, CWR
    tcp.ack = raspuns_syn_ack.seq + 1
    logging.info('Send ' + ch)
    rcv = sr1(ip/tcp/ch)
    tcp.seq += 1
    rcv.show()


tcp.flags = 'R' # RST
RES = ip/tcp
send(RES)
logging.info('Send RST and close')
