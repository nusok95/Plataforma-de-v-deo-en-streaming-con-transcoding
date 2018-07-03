import ffmpy
from transcoding.settings import MEDIA_ROOT

def transcode(archivo):
    entrada = MEDIA_ROOT+'/uploads/'+archivo
    print("VIDEO DE ENTRADA",entrada)
    archivo = archivo[:-3]
    salida = MEDIA_ROOT+'/uploads/'+archivo+'mp4'
    print(entrada,salida)
    ff = ffmpy.FFmpeg(
        inputs={entrada: None},
        outputs={salida: None})
    ff.run()