from datetime import datetime

# PORT_MAP = {
#     "445":"SMB"
# }

_TYPE = {
    "2048" : "IPv4",
    "2054":"ARP",
    "34525":"IPv6"
}

_PROTO = {
    "6":"TCP",
    "17":"UDP",
    "1":"ICMP",
    "2":"IGMP"
}

_ICMP_TYPE = {
    "8" : "echo-request",
    "0" : "echo-reply"
}

# Unpack ethernet frame
class ETHERNET_FRAME:
    def __init__(self, data):
        self.src = data.src
        self.dst = data.dst
        self.type = _TYPE[f'{data.type}']
        # self.time = datetime.strftime(datetime.now(), "%H:%M")
    
#Unpack IPv4 packet
class IPv4_PACKET:
    def __init__(self, data):
        self.version = data.version
        self.ihl = data.ihl
        self.tos = data.tos
        self.len = data.len
        self.id = data.id
        self.flags = data.flags
        self.frag = data.frag
        self.ttl = data.ttl
        self.proto = _PROTO[f'{data.proto}'] 
        self.chksum = data.chksum
        self.src = data.src
        self.dst = data.dst
        self.time = datetime.strftime(datetime.now(), "%H:%M")

#Unpacks TCP  packet
class TCP_SEGMENT:
    def __init__(self,data):
        self.sport = data.sport
        self.dport = data.dport
        self.seq = data.seq
        self.ack = data.ack
        self.dataofs = data.dataofs
        self.reserved = data.reserved
        self.flags = data.flags
        self.window = data.window
        self.chksum = data.chksum
        self.options = data.options
        # self.data = data[14:]
        # self.time = datetime.strftime(datetime.now(), "%H:%M")
    

#Unpacks UDP segment
class UDP_SEGMENT:
    def __init__(self, data):
        self.sport = data.sport
        self.dport = data.dport
        self.len = data.len
        self.chksum = data.chksum
        # self.time = datetime.strftime(datetime.now(), "%H:%M")
    

# #Unpacks ARP packet
class ARP_PACKET:
    def __init__(self, data):
        self.hwtype = data.hwtype
        self.ptype = data.ptype
        self.hwlen = data.hwlen
        self.plen = data.plen
        self.op = data.op
        self.hwsrc = data.hwsrc
        self.psrc = data.psrc
        self.hwdst = data.hwdst
        self.pdst = data.pdst

#Unpacks ICMP packet
class ICMP_PACKET:
    def __init__(self, data):
        self.type = _ICMP_TYPE[f'{data.type}']
        self.code = data.code
        self.chksum = data.chksum
        self.id = data.id
        self.seq = data.seq
        self.unused = data.unused
#         # self.time = datetime.strftime(datetime.now(), "%H:%M")

class RAW:
    def __init__(self, data):
        self.raw = data.load


