from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import FileAttributeSerializer
import os
import pwd
from datetime import datetime
from . import PasswordGenerator
from math import floor
from django.http import FileResponse
from rest_framework import status
import urllib.parse
import shutil


# Create your views here.
class FileAttributes:
    def __init__(self, name, st_size, st_ctime, st_atime, st_mtime, isdir, st_uid, st_gid, path):
        self.name = name
        self.st_size  = floor(st_size / 1024)
        self.st_ctime = datetime.fromtimestamp(st_ctime).strftime('%Y-%m-%d %H:%M')
        self.st_atime = datetime.fromtimestamp(st_atime).strftime('%Y-%m-%d %H:%M')
        self.st_mtime = datetime.fromtimestamp(st_mtime).strftime('%Y-%m-%d %H:%M')
        self.isdir = isdir
        self.st_uid = pwd.getpwuid(st_uid).pw_name
        self.st_gid = st_gid
        self.path = path

def list_dir(_dir, path):
    _data_ = []
    for name in _dir:
        if os.path.isdir(path + '/' + name):
            isdir = True
        else:
            isdir = False
        if isdir == True or name.endswith('.txt'):
            file_att = os.stat(path + '/' + name)
            selfpath = path + '/' + name

            data = FileAttributes(name, file_att.st_size, file_att.st_ctime,file_att.st_atime,file_att.st_mtime, isdir, file_att.st_uid, file_att.st_gid, selfpath)
            serializer = FileAttributeSerializer(data)
            _data_.append(serializer.data)
    return _data_

@api_view(['GET'])
def root_dir_child(request, path):
    if request.method == "GET":
        path = urllib.parse.unquote(path)
        if path.endswith('.txt'):
            return FileResponse(open(f'{path}', 'rb'),status=status.HTTP_200_OK)
        else:
            try:
                _dir = os.listdir(path)
            except FileNotFoundError:
                return Response({
                    "data":"No Such File or Directory",
                },status=status.HTTP_404_NOT_FOUND)
            _data_ = list_dir(_dir, path)

            return Response({
                "path": path,
                "data":_data_,
                },status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_file_or_dir(request, path):
    if request.method == "DELETE":
        path = urllib.parse.unquote(path)
        try:
            if path.endswith('.txt'):
                os.remove(path)
            else:
                shutil.rmtree(path)
            return Response({
                "data":"Success"
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                "data":"Can Not Remove!"
                }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_dir(request, path):
    if request.method == "POST":
        path = urllib.parse.unquote(path)
        try:
            _dir = path + '/' + request.data["name"]
            os.mkdir(f'{_dir}')
            return Response({
                "data":"Success"
                }, status=status.HTTP_201_CREATED)
        except FileExistsError:
            return Response({
                "data":"Bukjanyn Ady Eyyam Bar!"
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "data":"Can Not Create!"
                }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def rename_dir(request):
    if request.method == "PUT":
        try:
            old_name = request.data["old_name"]
            new_name = os.sep.join(old_name.split('/')[:-1:]) + '/' + request.data["new_name"]
            os.rename(old_name, new_name)
            return Response({
                "data":"Success"
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                "data":"Can Not Rename!"
                }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def createWordlist(request):
    if request.method == "POST":
        try:
            words = request.data['words']
            append_numbering = int(request.data['append_numbering'])
            numbering_limit = int(request.data['numbering_limit'])
            years = request.data['years']
            append_padding_post = request.data['append_padding']
            common_paddings_before_post = bool(request.data['common_paddings_before'])
            common_paddings_after_post = bool(request.data['common_paddings_after'])
            custom_paddings_only_post = request.data['custom_padding_only']
            outfile = request.data['filename']
            path = request.data["path"]

            outfile = path + '/' + outfile
            
            PasswordGenerator.generate_password(words, append_numbering,   
                                                numbering_limit, years, append_padding_post, 
                                                common_paddings_before_post, common_paddings_after_post, 
                                                custom_paddings_only_post, outfile)

            return Response({
                "data":"Successfully Created Wordlist"
                }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                "data":"Can Not Create WordList!"
                }, status=status.HTTP_400_BAD_REQUEST)
