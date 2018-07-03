import lxml
import os.path
import xmlschema
from tutub.settings import MEDIA_ROOT

BASE = os.path.dirname(os.path.abspath(__file__))

def validar(XML):
    scheme = xmlschema.XMLSchema(os.path.join(BASE, "usuarios.xsd"))
    if scheme.is_valid(XML):
        return True
    else:
        return False