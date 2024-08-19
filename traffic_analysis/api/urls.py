from django.urls import path, include, re_path
from traffic_analysis.api import views as api_view

urlpatterns = [
    path('', api_view.index, name=''),
    path('traffic', api_view.packet_sniffer, name='traffic'),
    path('start-packet-save', api_view.packet_save_start, name='start-packet-save'),
    path('stop-packet-save', api_view.packet_save_stop, name='start-packet-save'),
    path('pcap-reader', api_view.pcap_reader, name='pcap-reader'),
    path('pcap-download', api_view.pcap_download, name='pcap-download'),
    path('file-upload', api_view.file_upload, name='file-upload'),
    path('file-encrypt', api_view.file_encrypt, name='file-encrypt'),
    path('file-decrypt', api_view.file_decrypt, name='file-decrypt'),
]