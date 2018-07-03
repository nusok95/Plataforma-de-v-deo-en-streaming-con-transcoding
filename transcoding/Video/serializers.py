from .models import File
from rest_framework.serializers import ModelSerializer,FileField

class FileSerializer(ModelSerializer):
    file = FileField()
    class Meta:
        model = File
        fields = "__all__"

