"""
Clase SofaCama que implementa herencia múltiple.
Esta clase hereda tanto de Sofa como de Cama.
"""

from .sofa import Sofa
from .cama import Cama
from ..categorias.asientos import Asiento


class SofaCama(Sofa, Cama):
    """
    Clase que implementa herencia múltiple heredando de Sofa y Cama.

    Un sofá-cama es un mueble que funciona tanto como asiento durante el día
    como cama durante la noche.

    Conceptos OOP aplicados:
    - Herencia múltiple: Hereda de Sofa y Cama
    - Resolución MRO: Maneja el orden de resolución de métodos
    - Polimorfismo: Implementa comportamientos únicos combinando funcionalidades
    """

    TAMAÑOS_VALIDOS = ["single", "double", "queen", "king", "matrimonial"]

    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_personas: int = 3, material_tapizado: str = "tela",
                 tamaño_cama: str = "queen", incluye_colchon: bool = True,
                 mecanismo_conversion: str = "plegable"):
        """
        Constructor del sofá-cama.

        Args:
            capacidad_personas: Capacidad como sofá
            material_tapizado: Material del tapizado
            tamaño_cama: Tamaño cuando está desplegado como cama
            incluye_colchon: Si incluye colchón
            mecanismo_conversion: Tipo de mecanismo (plegable, corredizo, electrico)
        """
        Asiento.__init__(self, nombre, material, color, precio_base,
                         capacidad_personas=capacidad_personas,
                         tiene_respaldo=True,
                         material_tapizado=material_tapizado)
        self._es_modular = False
        self._tamaño_cama = tamaño_cama
        self._incluye_colchon = incluye_colchon
        self._mecanismo_conversion = mecanismo_conversion
        self._modo_actual = "sofa"

    @property
    def tamaño_cama(self) -> str:
        """Getter para el tamaño cuando es cama."""
        return self._tamaño_cama

    @property
    def incluye_colchon(self) -> bool:
        """Getter para si incluye colchón."""
        return self._incluye_colchon

    @property
    def mecanismo_conversion(self) -> str:
        """Getter para el tipo de mecanismo."""
        return self._mecanismo_conversion

    @property
    def modo_actual(self) -> str:
        """Getter para el modo actual (sofa o cama)."""
        return self._modo_actual

    @tamaño_cama.setter
    def tamaño_cama(self, value: str) -> None:
        """Setter para tamaño de cama con validación."""
        if value.lower() not in self.TAMAÑOS_VALIDOS:
            raise ValueError(f"Tamaño debe ser uno de: {self.TAMAÑOS_VALIDOS}")
        self._tamaño_cama = value

    @incluye_colchon.setter
    def incluye_colchon(self, value: bool) -> None:
        """Setter para colchón."""
        self._incluye_colchon = value

    @mecanismo_conversion.setter
    def mecanismo_conversion(self, value: str) -> None:
        """Setter para mecanismo."""
        self._mecanismo_conversion = value

    def calcular_precio(self) -> float:
        """
        Calcula el precio del sofá-cama combinando características de sofá y cama.

        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        precio *= self.calcular_factor_comodidad()
        precio *= (1.0 + (self.capacidad_personas - 1) * 0.2)
        tamaño_factor = {
            "single": 1.1, "double": 1.3, "queen": 1.5,
            "king": 1.7, "matrimonial": 1.5
        }
        precio *= tamaño_factor.get(self._tamaño_cama.lower(), 1.0)
        if self._incluye_colchon:
            precio *= 1.3
        if self._mecanismo_conversion.lower() == "electrico":
            precio *= 1.4
        elif self._mecanismo_conversion.lower() == "corredizo":
            precio *= 1.2
        else:
            precio *= 1.15
        return round(precio, 2)

    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del sofá-cama.

        Returns:
            str: Descripción detallada
        """
        descripcion = f"Sofá-Cama {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += f"Capacidad (sofá): {self.capacidad_personas} personas\n"
        descripcion += f"Tamaño (cama): {self._tamaño_cama}\n"
        descripcion += self.obtener_info_asiento() + "\n"
        descripcion += f"Incluye colchón: {'Sí' if self._incluye_colchon else 'No'}\n"
        descripcion += f"Mecanismo: {self._mecanismo_conversion}\n"
        descripcion += f"Modo actual: {self._modo_actual}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion

    def convertir_a_cama(self) -> str:
        """
        Convierte el sofá en cama.

        Returns:
            str: Mensaje del resultado de la conversión
        """
        if self._modo_actual == "cama":
            return "El sofá-cama ya está en modo cama"
        self._modo_actual = "cama"
        return f"Sofá convertido a cama usando mecanismo {self.mecanismo_conversion}"

    def convertir_a_sofa(self) -> str:
        """
        Convierte la cama en sofá.

        Returns:
            str: Mensaje del resultado de la conversión
        """
        if self._modo_actual == "sofa":
            return "El sofá-cama ya está en modo sofá"
        self._modo_actual = "sofa"
        return f"Cama convertida a sofá usando mecanismo {self.mecanismo_conversion}"

    def obtener_capacidad_total(self) -> dict:
        """
        Obtiene la capacidad tanto como sofá como cama.

        Returns:
            dict: Capacidades en ambos modos
        """
        camas = 1 if self._tamaño_cama.lower() == "single" else 2
        return {
            "como_sofa": self.capacidad_personas,
            "como_cama": camas
        }

    def __str__(self) -> str:
        """Representación en cadena del sofá-cama."""
        return f"Sofá-cama {self.nombre} (modo: {self._modo_actual})"
