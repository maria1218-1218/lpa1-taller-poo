"""
Clase concreta Escritorio.
Una superficie de trabajo especializada para oficina o estudio.
"""

from ..categorias.superficies import Superficie


class Escritorio(Superficie):
    """
    Clase concreta que representa un escritorio.
    
    Un escritorio es una superficie especializada para trabajo de oficina,
    típicamente con características como cajoneras, compartimientos, etc.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 largo: float, ancho: float, alto: float, material_superficie: str,
                 numero_cajones: int = 0, tiene_cajonera: bool = False,
                 altura_regulable: bool = False):
        """
        Constructor del escritorio.
        
        Args:
            numero_cajones: Número de cajones
            tiene_cajonera: Si tiene cajonera integrada
            altura_regulable: Si la altura es regulable
        """
        super().__init__(nombre, material, color, precio_base,
                        largo, ancho, alto, material_superficie)
        
        self._numero_cajones = numero_cajones
        self._tiene_cajonera = tiene_cajonera
        self._altura_regulable = altura_regulable
    
    @property
    def numero_cajones(self) -> int:
        """Getter para número de cajones."""
        return self._numero_cajones
    
    @property
    def tiene_cajonera(self) -> bool:
        """Getter para si tiene cajonera."""
        return self._tiene_cajonera
    
    @property
    def altura_regulable(self) -> bool:
        """Getter para si altura es regulable."""
        return self._altura_regulable
    
    @numero_cajones.setter
    def numero_cajones(self, value: int) -> None:
        """Setter para número de cajones."""
        if value < 0:
            raise ValueError("El número de cajones no puede ser negativo")
        self._numero_cajones = value
    
    @tiene_cajonera.setter
    def tiene_cajonera(self, value: bool) -> None:
        """Setter para cajonera."""
        self._tiene_cajonera = value
    
    @altura_regulable.setter
    def altura_regulable(self, value: bool) -> None:
        """Setter para altura regulable."""
        self._altura_regulable = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio del escritorio.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Factor por área
        area = self.calcular_area_superficie()
        precio *= (1.0 + (area / 1000 * 0.1))
        
        # Factor por material
        precio *= self.calcular_factor_material_superficie()
        
        # Premium por cajones
        precio += (self._numero_cajones * 50)
        
        # Premium si tiene cajonera
        if self._tiene_cajonera:
            precio *= 1.2
        
        # Premium si es regulable
        if self._altura_regulable:
            precio *= 1.15
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del escritorio.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Escritorio {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_superficie() + "\n"
        descripcion += f"Cajones: {self._numero_cajones}\n"
        descripcion += f"Cajonera: {'Sí' if self._tiene_cajonera else 'No'}\n"
        descripcion += f"Altura regulable: {'Sí' if self._altura_regulable else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
