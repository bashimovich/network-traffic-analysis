from rest_framework import serializers

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

class RawSerializer(serializers.Serializer):
    raw = serializers.CharField()