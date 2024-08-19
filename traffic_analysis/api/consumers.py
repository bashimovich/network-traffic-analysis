import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import EthernetFrameSerializer, Ipv4PacketSerializer, TcpSegmentSerializer, UdpSegmentSerializer, IcmpPacketSerializer, ArpPacketSerializer, RawSerializer
from scapy.all import *
from .PktParser import *

def traf_parser(pkt, data = {}):
    if "Ethernet" in pkt[0]:
        ethernet_frame_data = ETHERNET_FRAME(pkt[0]["Ethernet"])
        ethernet_frame_data = EthernetFrameSerializer(ethernet_frame_data)
        data["ethernet_frame_data"]=ethernet_frame_data.data

    if "IP" in pkt[0]:
        ipv4_packets = IPv4_PACKET(pkt[0]["IP"])
        ipv4_packets = Ipv4PacketSerializer(ipv4_packets)
        data["ipv4_packets"] = ipv4_packets.data

    if "TCP" in pkt[0]:
        protocols = TCP_SEGMENT(pkt[0]["TCP"])
        protocols = TcpSegmentSerializer(protocols)
        data["protocols"] = protocols.data
        
    elif "ARP" in pkt[0]:
        protocols = ARP_PACKET(pkt[0]["ARP"])
        protocols = ArpPacketSerializer(protocols)
        data["protocols"] = protocols.data

    elif "UDP" in pkt[0]:
        protocols = UDP_SEGMENT(pkt[0]["UDP"])
        protocols = UdpSegmentSerializer(protocols)
        data["protocols"] = protocols.data
    
    elif "ICMP" in pkt[0]:
        protocols = ICMP_PACKET(pkt[0]["ICMP"])
        protocols = IcmpPacketSerializer(protocols)
        data["protocols"] = protocols.data

    if "Raw" in pkt[0]:
        raw_data = RAW(pkt[0]["Raw"])
        raw = RawSerializer(raw_data)
        data["raw"] = raw.data
    return data


class NetworkTrafficHandlerTaksConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('traffic_hander_group', self.channel_name)
        await self.accept()
        self.pkts = []
        print('connetcted....')

    async def disconnect(self, code):
        await self.channel_layer.group_discard('traffic_hander_group', self.channel_name)
        print('disconnected...')

    async def network_traffic_handler(self, event):
        self.pkt = sniff(iface='enp1s0',count=1)
        self.data = {}
        
        # print("----------------------------------------------------------------")
        # self.pkt[0].show()
        # print("----------------------------------------------------------------")

        self.data = traf_parser(self.pkt[0], self.data)
        self.pkts.append(self.pkt)
        if event['task']:
            try:
                self.data = json.dumps(self.data, ensure_ascii=True)
                await self.send(self.data)
            except:
                await self.send({'message':'Can Not Capture Traffic!'})

    async def receive(self, text_data):
        self.filename = json.loads(text_data)["name"]
        self.path = './static/pcap/' + self.filename + '.pcap'
        wrpcap(self.path, self.pkts)
        self.pkts = []
        # self.path = json.dumps(self.path, ensure_ascii=True)
        # await self.send({'path' : self.path})
                