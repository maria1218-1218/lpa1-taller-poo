# necesario para que Python trate el directorio como un paquete

from .silla import Silla
from .sillon import Sillon
from .sofa import Sofa
from .sofacama import SofaCama
from .mesa import Mesa
from .escritorio import Escritorio
from .armario import Armario
from .cajonera import Cajonera
from .cama import Cama

__all__ = [
    "Silla",
    "Sillon",
    "Sofa",
    "SofaCama",
    "Mesa",
    "Escritorio",
    "Armario",
    "Cajonera",
    "Cama",
]
