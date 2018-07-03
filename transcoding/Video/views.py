from django.shortcuts import render
from .models import File
from rest_framework.serializers import FileField
from rest_framework.viewsets import ModelViewSet
from .serializers import FileSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .transcoding import transcode


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    def put(self, request):
        file_obj = request.FILES.get('file',None)
        archivo  = File(file = file_obj)
        print(file_obj)
        archivo.save()
        extension = "mp4"
        if not archivo.file.name.endswith(extension):
            try:
                transcode(file_obj.name)
            except:
                return Response(status=500)
        return Response(status=204)

