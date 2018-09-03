from scapy.all import *

eth = Ether(dst = 'ff:ff:ff:ff:ff:ff')
arp = ARP(pdst = '198.13.13.0/16')
answered,unanswered = srp(eth / arp,timeout = 1)

if answered:
    print answered[0][1].pdst, ' -- ', answered[0][1].hwdst

for answer in answered:
    print answer[1].psrc, ' -- ', answer[1].hwsrc

