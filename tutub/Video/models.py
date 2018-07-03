from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.utils.timezone import now

class Video(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=256,blank=True, null=True)
    archivo = models.FileField( validators=[FileExtensionValidator(["mp4","avi","mpeg","mov","wmv","flv","divx","mkv"])])
    usuario = models.ForeignKey(User, on_delete="cascade")
    thumbnail = models.FileField( blank=True, null=True, upload_to='thumbnails/',validators=[FileExtensionValidator(["png","jpg","jpeg","gif"])])
    busquedas = models.IntegerField(default = 0,blank=True, null=True)
    visitas = models.IntegerField(default = 0,blank=True, null=True)
    ruta = models.CharField(max_length=100,blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

class XML(models.Model):
    archivo = models.FileField(validators=[FileExtensionValidator(["xml"])])

class Notificacion(models.Model):
    usuario = models.ForeignKey(User,on_delete="cascade")
    contenido = models.CharField(max_length=256,blank=True, null=True)
    status = models.BooleanField()
    tipo = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)


