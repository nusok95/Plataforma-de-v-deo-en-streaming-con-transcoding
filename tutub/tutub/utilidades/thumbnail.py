from moviepy.editor import *
from tutub.settings import MEDIA_ROOT
import os

def crearThumb(video):
    clip = (VideoFileClip(MEDIA_ROOT+"/"+video.archivo.name)
            .subclip((0,00.65),(0,02.2))
            .resize(0.5))
    clip.write_gif(os.path.join(MEDIA_ROOT,'thumbnails')+'/'+video.archivo.name[:-3]+"gif")
    video.thumbnail = '/thumbnails/'+video.archivo.name[:-3]+"gif"
    video.save()
    return True
