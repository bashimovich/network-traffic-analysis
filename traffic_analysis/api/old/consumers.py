import json
from channels.generic.websocket import AsyncWebsocketConsumer
import socket
# from .sniffer import ETHERNET_FRAME, IPv4_PACKET, ICMP_PACKET, UDP_SEGMENT, TCP_SEGMENT
from .serializers import EthernetFrameSerializer, Ipv4PacketSerializer, TcpSegmentSerializer, UdpSegmentSerializer, IcmpPacketSerializer, ArpPacketSerializer
from scapy.all import *
from asgiref.sync import async_to_sync
from PktParser import *

class NetworkTrafficHandlerTaksConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('traffic_hander_group', self.channel_name)
        # self.conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        # self.conn.bind(('enp1s0',0))
        await self.accept()
        self.pkts = []
        print('connetcted....')

    async def disconnect(self, code):
        await self.channel_layer.group_discard('traffic_hander_group', self.channel_name)
        print('disconnected...')

    async def network_traffic_handler(self, event):
        pkt = sniff(iface='enp1s0',count=1)
        data = {}
        print("----------------------------------------------------------------")
        pkt[0].show()
        print("----------------------------------------------------------------")
        if "Ethernet" in pkt[0]:
            print('Ethernet')
            ethernet_frame_data = ETHERNET_FRAME(pkt[0]["Ethernet"])
            ethernet_frame_data = EthernetFrameSerializer(ethernet_frame_data)
            data["ethernet_frame_data"]=ethernet_frame_data.data

        if "IP" in pkt[0]:
            print("IP")
            ipv4_packets = IPv4_PACKET(pkt[0]["IP"])
            ipv4_packets = Ipv4PacketSerializer(ipv4_packets)
            data["ipv4_packets"] = ipv4_packets.data

        if "TCP" in pkt[0]:
            print("TCP")
            protocols = TCP_SEGMENT(pkt[0]["TCP"])
            protocols = TcpSegmentSerializer(protocols)
            data["protocols"] = protocols.data
            
        if "ARP" in pkt[0]:
            print("ARP")
            protocols = ARP_PACKET(pkt[0]["ARP"])
            protocols = ArpPacketSerializer(protocols)
            data["protocols"] = protocols.data

        if "UDP" in pkt[0]:
            print("UDP")
            protocols = UDP_SEGMENT(pkt[0]["UDP"])
            protocols = UdpSegmentSerializer(protocols)
            data["protocols"] = protocols.data
        
        if "ICMP" in pkt[0]:
            print("ICMP")
            protocols = ICMP_PACKET(pkt[0]["ICMP"])
            protocols = IcmpPacketSerializer(protocols)
            data["protocols"] = protocols.data
        # print(pkt.hexdump())
        # self.pkts.append(pkt)
        if event['task']:
            try:
                # raw_data, addr = self.conn.recvfrom(65536)
                # ef = ETHERNET_FRAME(raw_data)
                # ethernet_frame_serializer = EthernetFrameSerializer(ef)
                # # pkt = sniff(iface='enp1s0',count=1)
                # # self.pkts.append(pkt)
                # #8bit for IPv4
                # if ef.proto == 8:
                #     ipv4_p = IPv4_PACKET(ef.data)
                #     ip_packet_serializer = Ipv4PacketSerializer(ipv4_p)

                #     if ipv4_p.proto == 1:
                #         icmp_p = ICMP_PACKET(ipv4_p.data)
                #         protocols_serializer = IcmpPacketSerializer(icmp_p)

                #     elif ipv4_p.proto == 6:
                #         tcp_p = TCP_SEGMENT(ipv4_p.data)
                #         protocols_serializer = TcpSegmentSerializer(tcp_p)

                #     elif ipv4_p.proto == 17:
                #         udp_p = UDP_SEGMENT(ipv4_p.data)
                #         protocols_serializer = UdpSegmentSerializer(udp_p)


                data = json.dumps(data, ensure_ascii=True)
                await self.send(data)

            except:
                await self.send({'message':'Can Not Capture Traffic!'})

    async def receive(self, text_data):
        filename = json.loads(text_data)["name"]
        wrpcap(f"{filename}.pcap", self.pkts)
        self.pkts = []