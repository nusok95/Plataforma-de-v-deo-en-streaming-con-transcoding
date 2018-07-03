from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Template
from .forms import VideoForm, RegistroForm, XMLForm
from .settings import SERVER_URL, SERVER_URL_MEDIA
from Video.models import Video,Notificacion
from tutub.validacion.importar import xml_to_bd
from tutub.utilidades.thumbnail import crearThumb
import requests
import json



def home(request):
    return render_to_response("base.html")


def entrar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/videos/')
        else:
            return render(request,"login.html")
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/videos/')
        else:
            return render(request,'login.html',{'mensaje':'error'})


def registro(request):
    if request.method == 'GET':
        form = RegistroForm(use_required_attribute=False)
        return render(request, 'registro.html', {'form':form})
    elif request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            email = request.POST.get('email',None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            try:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return render(request, 'login.html', {'form':form})
            except:
                return render(request, 'registro.html', {'form':'Todo bien krnal'})
        else:
            form = RegistroForm(request.POST)
            return render(request, 'registro.html',{'form':form})
            
def salir(request):
    logout(request)
    return redirect('/videos/')

@login_required
def subir(request):
    if request.method == 'GET':
        form = VideoForm()
        #use_required_attribute=False
        return render(request, 'subir_video.html', {'form': form})
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = request.POST.get('nombre',None)
            noti2 = Notificacion(usuario = request.user, contenido = "Subiendo vídeo "+ str(nombre)  , status = 1, tipo = 0)
            noti2.save()
            descripcion = request.POST.get('descripcion',None)
            archivo = request.FILES.get('archivo',None)
            usuario = request.user
            thumbnail = request.FILES.get('thumbnail',None)
            video = Video(nombre = nombre, descripcion = descripcion, archivo = archivo, usuario = usuario, thumbnail = thumbnail)
            video.save()
            if thumbnail == None:
                crearThumb(video)
            ruta = video.archivo.name[:-3]
            video.ruta = (ruta+'mp4')
            video.save()
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
            'Media-Type':'multipart/form-data'}
            files={'file':video.archivo}
            '''try:
                r = requests.put(SERVER_URL+'/videos/', headers = headers , files = files)
                noti = Notificacion(usuario = request.user, contenido = "Procesando vídeo "+ str(nombre)  , status = 1, tipo = 0)
                noti.save()
            except:
                mensaje = "No se pudo procesar tu vídeo "+ str(nombre) +", intentalo de nuevo"
                noti = Notificacion(usuario = request.user, contenido = "No se pudo procesar tu vídeo "+ str(nombre)  , status = 0, tipo = 1)
                noti2 = Notificacion.objects.filter(tipo = 0).delete()
                noti.save()
                video = Video.objects.get(id = video.id).delete()
                status = 'error'
                return render(request, 'subir_video.html', {'form':form,'mensaje':mensaje,'status':status})'''
            mensaje = "Tú vídeo ahora se encuentra listo, los demás usuarios pueden verlo"
            noti = Notificacion(usuario = request.user, contenido = "Tu vídeo "+ str(nombre) +" ahora se encuentra listo" , status = 1, tipo = 1)
            noti.save()
            noti2 = Notificacion.objects.filter(tipo = 0).delete()
            status = 'success'
            return render(request, 'subir_video.html', {'form':form,'mensaje':mensaje,'status':status})    
        else:
            form = VideoForm(request.POST,request.FILES)
            return render(request, 'subir_video.html', {'form': form})    
    else:
        form = VideoForm(request.POST,request.FILES)

    return render(request, 'subir_video.html', {'form': form})
        

def videos_mostrados(request):
    try:
        videos = Video.objects.all()
        context = {'videos':videos}
        return render(request,"videos.html",context)
    except:
        return render(request,"videos.html")

def busqueda(request):
    video = request.POST.get('nombre_video',None)
    if video.strip != '':
        videos = Video.objects.filter(nombre__icontains=video)
        for vid in videos:
            vid.busquedas = vid.busquedas + 1
            vid.save()
        contexto = {'videos':videos,'resultado':True,'busqueda':video}
    else:
        contexto = {'resultado':False}
    return render(request, 'videos.html',contexto)

def video_detalle(request,id_video):
    try:
        video = Video.objects.get(id = id_video)
        video.visitas = video.visitas + 1
        video.save()
        return render(request, 'video_detalle.html',{'video':video,'MEDIA':SERVER_URL_MEDIA})
    except:
        return render(request,'videos.html')

def filtrar(request,filtro):
    if filtro == 'vistos':
        videos = Video.objects.all().order_by('-visitas')
        return render(request,'videos.html',{'videos':videos})
    if filtro == 'recientes':
        videos = Video.objects.all().order_by('-fecha_publicacion')
        return render(request,'videos.html',{'videos':videos})
    if filtro == 'buscados':
        videos = Video.objects.all().order_by('-busquedas')
        return render(request,'videos.html',{'videos':videos})
    else:
        videos = Video.objects.all()
        return render(request,'videos.html',{'videos':videos})

@login_required
def importar_usuarios(request):
    if not request.user.is_superuser:
        return redirect('/videos/')
    if request.method == 'GET':
        form = XMLForm()
        return render(request, 'importar_usuarios.html', {'form':form})
    elif request.method == 'POST':
        form = XMLForm(request.POST,request.FILES)
        if form.is_valid():
            archivo = request.FILES.get('archivo',None)
            noti = Notificacion(usuario = request.user, contenido = "Importando usuarios" , status = 1, tipo = 0)
            noti.save()
            mensaje = xml_to_bd(archivo)
            if 'success' in mensaje.keys():
                mensaje = mensaje['success']
                noti = Notificacion(usuario = request.user, contenido = "Usuarios importados correctamente" , status = 1, tipo = 1)
                noti.save()
                status = 'success'
            else:
                mensaje = mensaje['error']
                status = 'error'
                noti = Notificacion(usuario = request.user, contenido = "Error al importar usuarios" , status = 0, tipo = 1)
                noti.save()
            noti2 = Notificacion.objects.filter(tipo = 0).delete()
            return render(request, 'importar_usuarios.html', {'form':form,'mensaje':mensaje,'status':status})
            
        else:
            form = XMLForm(request.POST)
            return render(request, 'importar_usuarios.html',{'form':form})
            
@login_required    
def mis_videos(request):
    try:
        videos = Video.objects.filter(usuario = request.user)
        context = {'videos':videos}
        return render(request,"videos.html",context)
    except:
        return redirect('/videos/')
    
def obtenernotificaciones(request):
    if request.user:
        notificaciones = obtenerNoti(request.user)
        notificacionesSerializadas = [ serializadornotificaciones(notificacion) for notificacion in notificaciones ]
        return HttpResponse(json.dumps(notificacionesSerializadas), content_type='application/json')
    else:
        notificacionesNulas = {'contenido': 'vacio'}
        return HttpResponse(json.dumps(notificacionesNulas), content_type='application/json; encoding=utf-8')

def serializadornotificaciones(notificacion):
    return {'contenido': notificacion.contenido,'status':notificacion.status,'tipo':notificacion.tipo}
    
def obtenerNoti(user):
    notificaciones = Notificacion.objects.filter(usuario=user).order_by('-fecha')[:4]
    return notificaciones    
