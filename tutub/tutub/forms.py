from django.forms import ModelForm, TextInput, FileInput, Textarea, forms,PasswordInput
from Video.models import Video,XML
from django.template.defaultfilters import filesizeformat
from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator 
 
class VideoForm(ModelForm):
    archivo = forms.FileField(validators=[FileExtensionValidator(["mp4","avi","mpeg","mov","wmv","flv","divx","mkv"])])
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['nombre'].max_length = 50
        self.fields['nombre'].help_text = "Este nombre será mostrado a los demás usuarios"
        self.fields['nombre'].error_messages = {'required': "Este campo es requerido"}
        self.fields['descripcion'].required = False
        self.fields['descripcion'].max_length = 50
        self.fields['descripcion'].help_text = "No es necesario que la pongas :v"
        self.fields['thumbnail'].help_text = "Si no escoges un thumbnail el sistema escogerá uno que forme parte de tu vídeo"
        self.fields['thumbnail'].required = False
    class Meta:
        """Meta definition for Videoform."""
        model = Video
        fields = ('nombre','descripcion','archivo','thumbnail')
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'El Nombre de tu vídeo','novalidate':''}),
            'descripcion': Textarea(attrs={'placeholder':'Agrega una breve descripción del vídeo'}),
            'archivo': FileInput(attrs={'class':'inputfile-1','accept':"video/*"}),
            'thumbnail': FileInput(attrs={'class':'inputfile-1','accept':"image/*"}),
            }

class RegistroForm(ModelForm):
    password= forms.CharField(widget=PasswordInput())
    confirmar_password=forms.CharField(widget=PasswordInput())

    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['username'].max_length = 50
        self.fields['username'].error_messages = {'required': "Este campo es requerido"}
        
    class Meta:
        """Meta definition for Videoform."""
        model = User
        fields = ('first_name','last_name','username','email','password')
    
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden, deben ser iguales"
            )

class XMLForm(ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(XMLForm, self).__init__(*args, **kwargs)
        self.fields['archivo'].required = True
        self.fields['archivo'].help_text = "Selecciona el archivo para importar usuarios"
        self.fields['archivo'].error_messages = {'required': "Selecciona un archivo para importar usuarios"}
    

    class Meta:
        """Meta definition for Videoform."""
        model = XML
        fields = ('__all__')
        widgets = {
            'archivo': FileInput(attrs={'class':'inputfile-1','accept':"text/xml"}),
            }
    