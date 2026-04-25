"""
Clase concreta Sofa.
Un asiento multiseat con capacidad para varias personas.
"""

from ..categorias.asientos import Asiento


class Sofa(Asiento):
    """
    Clase concreta que representa un sofá.
    
    Un sofá es un asiento para múltiples personas con características
    como capacidad variable, chaisés, etc.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_personas: int = 3, material_tapizado: str = "tela",
                 es_modular: bool = False):
        """
        Constructor del sofá.
        
        Args:
            capacidad_personas: Número de personas que se pueden sentar
            material_tapizado: Material del tapizado
            es_modular: Si el sofá es modular
        """
        super().__init__(nombre, material, color, precio_base,
                        capacidad_personas=capacidad_personas, 
                        tiene_respaldo=True,
                        material_tapizado=material_tapizado)
        
        self._es_modular = es_modular
    
    @property
    def es_modular(self) -> bool:
        """Getter para si es modular."""
        return self._es_modular
    
    @es_modular.setter
    def es_modular(self, value: bool) -> None:
        """Setter para modular."""
        self._es_modular = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio del sofá.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Aplicar factor de comodidad
        precio *= self.calcular_factor_comodidad()
        
        # Premium por capacidad
        precio *= (1.0 + (self.capacidad_personas - 1) * 0.2)
        
        # Premium si es modular
        if self._es_modular:
            precio *= 1.25
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del sofá.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Sofá {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_asiento() + "\n"
        descripcion += f"Modular: {'Sí' if self._es_modular else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
