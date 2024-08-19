from rest_framework import serializers

class FileAttributeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    st_size = serializers.FloatField()
    st_ctime = serializers.DateField()
    st_atime = serializers.DateField()
    st_mtime = serializers.DateField()
    isdir = serializers.BooleanField()
    st_uid = serializers.CharField(max_length=100)
    st_gid = serializers.CharField(max_length=100)
    path = serializers.CharField(max_length=300)