import xmltodict as xd
from django.contrib.auth.models import User
from django.db import IntegrityError
from tutub.validacion.XML_Validate import validar
from tutub.settings import MEDIA_ROOT 

def xml_to_bd(archivo):
    diccionario = archivo.read()
    XML = diccionario


    if validar(XML):    
        diccionario = xd.parse(diccionario)
        diccionario = diccionario["tutub"]
        
        usuarios = diccionario["usuario"]
        
        if type(usuarios) != list:
            first_name = (usuarios['first_name'])
            last_name = (usuarios['last_name'])
            username = (usuarios['username'])
            email = (usuarios['email'])
            password = (usuarios['password'])
            is_superuser = (usuarios['is_superuser'])
            
            try:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                mensaje = {'success':"Usuario importado correctamente"}
                return(mensaje)
            except IntegrityError:
                mensaje = {'error':"Error, el usuario ya existe"}
                return(mensaje)

        else:
            for usuario in usuarios:
                first_name = (usuario['first_name'])
                last_name = (usuario['last_name'])
                username = (usuario['username'])
                email = (usuario['email'])
                password = (usuario['password'])
                is_superuser = (usuario['is_superuser'])
                try: 
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_superuser = is_superuser)
                    user.save()
                    mensaje = {'success':'Usuarios importados correctamente'}
                except IntegrityError:
                    mensaje = {'error':"Error, usuario o usuarios ya existentes"}
            return(mensaje)
    else:
        mensaje = {'error':"Tu XML no es válido, por favor introduce uno válido"}
        return (mensaje)





  
    