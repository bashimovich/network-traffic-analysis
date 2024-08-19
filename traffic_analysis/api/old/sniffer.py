import socket
import struct
import textwrap
from datetime import datetime

# PORT_MAP = {
#     "445":"SMB"
# }

#Returns properly formatted IPv4 address(127.0.0.1)
def ipv4(addr):
    return '.'.join(map(str, addr))

#return properly formatted MAC address(ei AA:VV:BB:J3:EE:FF:DD:OO)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()
    
#Formats multi-line data
def format_multi_line(prefix, string, size=80):
    seize -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
        return '\n'.join()([prefix + line for line in textwrap.wrap(string, size)])

# Unpack ethernet frame
class ETHERNET_FRAME:
    def __init__(self, data):
        dest_mac , src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
        self.dest_mac = get_mac_addr(dest_mac)
        self.src_mac = get_mac_addr(src_mac)
        self.proto = socket.htons(proto)
        self.data = data[14:]
        # self.time = datetime.strftime(datetime.now(), "%H:%M")

#Unpacks TCP  packet
class TCP_SEGMENT:
    def __init__(self,data):
        (source_port, dest_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
        self.protocol_name = 'TCP'
        self.source_port = source_port
        self.dest_port = dest_port
        self.sequence = sequence
        self.acknowledgement = acknowledgement
        self.offset = (offset_reserved_flags >> 12) * 4
        self.flag_urg = (offset_reserved_flags & 32) >> 5 
        self.flag_ack = (offset_reserved_flags & 16) >> 4 
        self.flag_psh = (offset_reserved_flags & 8) >> 3 
        self.flag_rst = (offset_reserved_flags & 4) >> 2 
        self.flag_syn = (offset_reserved_flags & 2) >> 1 
        self.flag_fin = offset_reserved_flags & 1 
        self.data = data[14:]
        # self.time = datetime.strftime(datetime.now(), "%H:%M")
    

#Unpacks UDP segment
class UDP_SEGMENT:
    def __init__(self, data):
        src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
        self.protocol_name = 'UDP'
        self.src_port = src_port
        self.dest_port = dest_port
        self.size = size
        self.data = data[8:]
        # self.time = datetime.strftime(datetime.now(), "%H:%M")
    

#Unpacks ICMP packet
class ICMP_PACKET:
    def __init__(self, data):
        icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
        self.protocol_name = 'ICMP'
        self.icmp_type = icmp_type
        self.code = code
        self.checksum = checksum
        self.data  = data[4:]
        # self.time = datetime.strftime(datetime.now(), "%H:%M")

    
#Unpack IPv4 packet
class IPv4_PACKET:
    def __init__(self, data):
        version_header_length = data[0]
        version = version_header_length >> 4
        header_length = (version_header_length & 15) * 4
        ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
        self.version = version
        self.header_length = header_length
        self.ttl = ttl
        self.proto = proto
        self.src = ipv4(src)
        self.target = ipv4(target)
        self.data = data[header_length:]
        self.time = datetime.strftime(datetime.now(), "%H:%M")
