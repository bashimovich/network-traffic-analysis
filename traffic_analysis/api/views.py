from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from  scapy.all import *
from .ReadWritePcap import *
from .consumers import traf_parser
from django.shortcuts import render
from .EncrypC import *

def handle_uploaded_file(f, chunk, path):
    if int(chunk) > 0:
        # opens for append
        _file = open(path,  'ab')
    else:
        # erases content
        _file = open(path, 'wb')
    if f.multiple_chunks:
        for chunk in f.chunks():
            _file.write(chunk)
    else:
        _file.write(f.read())

def index(request):
    return render(request, 'room.html')

@api_view(['GET'])
def packet_sniffer(request):
    if request.method == "GET":
        return Response({
            "message":"Success Message Here!!!"
        })

@api_view(['GET'])
def packet_save_start(request):
    if request.method == "GET":
        return Response({
            "message":"Save Packet Start!!!"
        })

@api_view(['GET'])
def packet_save_stop(request):
    if request.method == "GET":
        return Response({
            "message":"Save Packet Stop!!!"
        })

@api_view(['POST'])
def pcap_reader(request):
    if request.method == "POST":
        path = './static/pcap/'+str(request.data['name'])
        pkts = rdpcap(path)
        data_pack = []
        for pkt in pkts:
            parsed_pkt = traf_parser(pkt)
            data_pack.append(parsed_pkt)
        return Response({
            "data": data_pack
        })

def file_iterator(file, chunk_size = 512):
    with open(file, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
        f.close()

@api_view(['POST'])
def pcap_download(request):
    if request.method == "POST":
        link = '/media/pcap/' + str(request.data['name']) + '.pcap'
        return Response({
            "data": link
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def file_encrypt(request):
    if request.method == "POST":
        path = f'./upload/'+str(request.data['name'])
        key = request.data["key"]
        _dir = request.data['dir']
        enc = EncryptionTool(path, _dir, key)
        enc_file = enc.encrypt()
        link = '/media/' + enc_file
        return Response({
            "data": link
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def file_decrypt(request):
    if request.method == "POST":
        path = f'./upload/'+str(request.data['name'])
        key = request.data["key"]
        _dir = request.data['dir']
        enc = EncryptionTool(path, _dir, key)
        dec_file = enc.decrypt()
        link = '/media/' + dec_file
        return Response({
            "data": link
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def file_upload(request):
    if request.method == "POST":
        name = request.data['name']
        extention = name.split('.')[-1]
        if extention == 'pcap' or extention == 'pcapng':
            path = f"./static/pcap/"+ str(name)
        else:
            path = f"./upload/"+ str(name)

        for _file in request.FILES:
            handle_uploaded_file(request.FILES[_file],
                                request.POST.get('chunk', 0),
                                path)
        if request.data['is_last'] in 'true':
            return Response({
                "data": name
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": "Uploading...",
            }, status=status.HTTP_200_OK)