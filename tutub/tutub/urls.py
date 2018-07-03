"""tutub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', videos_mostrados),
    url(r'^login', entrar),
    url(r'^registro', registro),
    url(r'^logout', salir),
    url(r'^upload', login_required(subir)),
    url(r'^videos', videos_mostrados),
    url(r'^search', busqueda),
    url(r'^mis_videos', login_required(mis_videos)),
    url(r'^importar_usuarios', login_required(importar_usuarios)),
    url(r'^obtenernotificaciones', obtenernotificaciones),
    url(r'^video/(?P<id_video>\d+)/$', video_detalle),
    url(r'^filtro/(?P<filtro>\w+)/$', filtrar),
    url(r'^progressbarupload/', include('progressbarupload.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
