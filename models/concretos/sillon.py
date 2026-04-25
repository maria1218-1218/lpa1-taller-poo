"""
Clase concreta Sillón.
Un asiento cómodo individual más grande que una silla.
"""

from ..categorias.asientos import Asiento


class Sillon(Asiento):
    """
    Clase concreta que representa un sillón.
    
    Un sillón es un asiento individual de mayor tamaño y comodidad que una silla,
    típicamente con brazos y respaldo acolchado.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 tiene_brazos: bool = True, material_tapizado: str = "tela"):
        """
        Constructor del sillón.
        
        Args:
            tiene_brazos: Si el sillón tiene brazos
            material_tapizado: Material del tapizado (por defecto tela)
        """
        # Llamar al constructor padre con capacidad de 1 persona
        super().__init__(nombre, material, color, precio_base,
                        capacidad_personas=1, tiene_respaldo=True,
                        material_tapizado=material_tapizado)
        
        self._tiene_brazos = tiene_brazos
    
    @property
    def tiene_brazos(self) -> bool:
        """Getter para si tiene brazos."""
        return self._tiene_brazos
    
    @tiene_brazos.setter
    def tiene_brazos(self, value: bool) -> None:
        """Setter para brazos."""
        self._tiene_brazos = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio del sillón.
        Los sillones son más caros que las sillas por su comodidad.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Aplicar factor de comodidad base
        precio *= self.calcular_factor_comodidad()
        
        # Sillones tienen premium de comodidad
        precio *= 1.3
        
        # Agregar costo por brazos
        if self._tiene_brazos:
            precio *= 1.15
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del sillón.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Sillón {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_asiento() + "\n"
        descripcion += f"Con brazos: {'Sí' if self._tiene_brazos else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
