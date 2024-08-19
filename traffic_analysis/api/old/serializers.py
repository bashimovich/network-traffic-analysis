from rest_framework import serializers

# class TcpSegmentSerializer(serializers.Serializer):
#     protocol_name = serializers.CharField(max_length = 50)
#     source_port = serializers.CharField(max_length=100)
#     dest_port = serializers.CharField(max_length=100)
#     acknowledgement = serializers.CharField(max_length=100)
#     sequence = serializers.CharField(max_length=100)
#     offset = serializers.CharField(max_length=100)
#     flag_urg = serializers.CharField(max_length=10)
#     flag_ack = serializers.CharField(max_length=10)
#     flag_psh = serializers.CharField(max_length=10)
#     flag_rst = serializers.CharField(max_length=10)
#     flag_syn = serializers.CharField(max_length=10)
#     flag_fin = serializers.CharField(max_length=10)
#     data = serializers.CharField()
#     # time = serializers.DateField()

# class UdpSegmentSerializer(serializers.Serializer):
#     protocol_name = serializers.CharField(max_length = 50)
#     src_port = serializers.CharField(max_length=10)
#     dest_port = serializers.CharField(max_length=10)
#     size = serializers.CharField(max_length=100)
#     data = serializers.CharField()
#     # time = serializers.DateField()

# class EthernetFrameSerializer(serializers.Serializer):
#     dest_mac = serializers.CharField(max_length = 50)
#     src_mac = serializers.CharField(max_length = 50)
#     proto = serializers.CharField(max_length = 50)
#     # data = serializers.CharField()
#     # time = serializers.DateField()

# class Ipv4PacketSerializer(serializers.Serializer):
#     version = serializers.CharField(max_length=100)
#     header_length = serializers.CharField(max_length=100)
#     ttl = serializers.CharField(max_length=100)
#     src = serializers.IPAddressField()
#     target = serializers.IPAddressField()
#     time = serializers.DateField()
#     # data = serializers.CharField()

# class IcmpPacketSerializer(serializers.Serializer):
#     protocol_name = serializers.CharField(max_length = 50)
#     icmp_type = serializers.CharField(max_length=10)
#     code = serializers.CharField(max_length=10)
#     checksum = serializers.CharField(max_length=10)
#     data = serializers.CharField()

class TcpSegmentSerializer(serializers.Serializer):
    sport = serializers.CharField(max_length=100)
    dport = serializers.CharField(max_length=100)
    seq = serializers.CharField(max_length=100)
    ack = serializers.CharField(max_length=100)
    dataofs = serializers.CharField(max_length=100)
    reserved = serializers.CharField(max_length=100)
    flags = serializers.CharField(max_length=10)
    window = serializers.CharField(max_length=10)
    chksum = serializers.CharField(max_length=10)
    # data = serializers.CharField()
    # time = serializers.DateField()

class UdpSegmentSerializer(serializers.Serializer):
    sport = serializers.CharField(max_length = 50)
    dport = serializers.CharField(max_length=10)
    len = serializers.CharField(max_length=10)
    chksum = serializers.CharField(max_length=100)
    # time = serializers.DateField()

class EthernetFrameSerializer(serializers.Serializer):
    src = serializers.CharField(max_length = 50)
    dst = serializers.CharField(max_length = 50)
    type = serializers.CharField(max_length = 50)
    # data = serializers.CharField()
    # time = serializers.DateField()

class Ipv4PacketSerializer(serializers.Serializer):
    version = serializers.CharField(max_length=100)
    ihl = serializers.CharField(max_length=100)
    tos = serializers.CharField(max_length=100)
    len = serializers.CharField(max_length=100)
    id = serializers.CharField(max_length=100)
    flags = serializers.CharField(max_length=100)
    frag = serializers.CharField(max_length=100)
    ttl = serializers.CharField(max_length=100)
    proto = serializers.CharField(max_length=100)
    ttl = serializers.CharField(max_length=100)
    chksum = serializers.CharField(max_length=100)
    src = serializers.IPAddressField()
    dst = serializers.IPAddressField()
    time = serializers.DateField()
    # data = serializers.CharField()

class IcmpPacketSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=10)
    chksum = serializers.CharField(max_length=10)
    id = serializers.CharField(max_length=10)
    seq = serializers.CharField(max_length=10)
    unused = serializers.CharField(max_length=10)

class ArpPacketSerializer(serializers.Serializer):
    hwtype = serializers.CharField(max_length=10)
    ptype = serializers.CharField(max_length=10)
    hwlen = serializers.CharField(max_length=10)
    plen = serializers.CharField(max_length=10)
    op = serializers.CharField(max_length=10)
    hwsrc = serializers.CharField(max_length=10)
    psrc = serializers.CharField(max_length=10)
    hwdst = serializers.CharField(max_length=10)
    pdst = serializers.CharField(max_length=10)