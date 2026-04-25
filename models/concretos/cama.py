"""
Clase concreta Cama.
Mueble para dormir.
"""

from ..categorias.asientos import Asiento


class Cama(Asiento):
    """
    Clase concreta que representa una cama.
    
    Una cama es un mueble diseñado para dormir, con características como
    tamaño, tipo de colchón, almacenamiento bajo cama, etc.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 tamaño: str = "queen", tiene_almacenamiento: bool = False,
                 es_electrica: bool = False):
        """
        Constructor de la cama.
        
        Args:
            tamaño: Tamaño de la cama (single, double, queen, king)
            tiene_almacenamiento: Si tiene almacenamiento bajo la cama
            es_electrica: Si la cama tiene control eléctrico
        """
        # Mapear tamaño a capacidad de personas
        capacidad_map = {"single": 1, "double": 2, "queen": 2, "king": 2}
        capacidad = capacidad_map.get(tamaño.lower(), 2)
        
        super().__init__(nombre, material, color, precio_base,
                        capacidad_personas=capacidad, 
                        tiene_respaldo=False,
                        material_tapizado="algodón")
        
        self._tamaño = tamaño
        self._tiene_almacenamiento = tiene_almacenamiento
        self._es_electrica = es_electrica
    
    @property
    def tamaño(self) -> str:
        """Getter para el tamaño."""
        return self._tamaño
    
    @property
    def tiene_almacenamiento(self) -> bool:
        """Getter para si tiene almacenamiento."""
        return self._tiene_almacenamiento
    
    @property
    def es_electrica(self) -> bool:
        """Getter para si es eléctrica."""
        return self._es_electrica
    
    @tamaño.setter
    def tamaño(self, value: str) -> None:
        """Setter para tamaño."""
        tamaños_validos = ["single", "double", "queen", "king"]
        if value.lower() not in tamaños_validos:
            raise ValueError(f"Tamaño debe ser uno de: {tamaños_validos}")
        self._tamaño = value
    
    @tiene_almacenamiento.setter
    def tiene_almacenamiento(self, value: bool) -> None:
        """Setter para almacenamiento."""
        self._tiene_almacenamiento = value
    
    @es_electrica.setter
    def es_electrica(self, value: bool) -> None:
        """Setter para eléctrica."""
        self._es_electrica = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio de la cama.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Factor por tamaño
        tamaño_factor = {"single": 1.0, "double": 1.3, "queen": 1.5, "king": 1.7}
        precio *= tamaño_factor.get(self._tamaño.lower(), 1.0)
        
        # Premium por almacenamiento
        if self._tiene_almacenamiento:
            precio *= 1.2
        
        # Premium por control eléctrico
        if self._es_electrica:
            precio *= 1.4
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa de la cama.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Cama {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += f"Tamaño: {self._tamaño}\n"
        descripcion += f"Capacidad: {self.capacidad_personas} personas\n"
        descripcion += f"Almacenamiento: {'Sí' if self._tiene_almacenamiento else 'No'}\n"
        descripcion += f"Eléctrica: {'Sí' if self._es_electrica else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
