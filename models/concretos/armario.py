"""
Clase concreta Armario.
Mueble de almacenamiento para ropa y objetos.
"""

from ..categorias.almacenamiento import Almacenamiento


class Armario(Almacenamiento):
    """
    Clase concreta que representa un armario.
    
    Un armario es un mueble de almacenamiento especializado para guardar ropa
    y otros objetos, con características como puertas, perchas, etc.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_volumen: float, numero_compartimientos: int,
                 tiene_espejo: bool = False, numero_puertas: int = 1):
        """
        Constructor del armario.
        
        Args:
            tiene_espejo: Si el armario tiene espejo
            numero_puertas: Número de puertas
        """
        super().__init__(nombre, material, color, precio_base,
                        capacidad_volumen, numero_compartimientos,
                        tiene_cerraduras=True)
        
        self._tiene_espejo = tiene_espejo
        self._numero_puertas = numero_puertas
    
    @property
    def tiene_espejo(self) -> bool:
        """Getter para si tiene espejo."""
        return self._tiene_espejo
    
    @property
    def numero_puertas(self) -> int:
        """Getter para número de puertas."""
        return self._numero_puertas
    
    @tiene_espejo.setter
    def tiene_espejo(self, value: bool) -> None:
        """Setter para espejo."""
        self._tiene_espejo = value
    
    @numero_puertas.setter
    def numero_puertas(self, value: int) -> None:
        """Setter para número de puertas."""
        if value < 1:
            raise ValueError("Debe haber al menos 1 puerta")
        self._numero_puertas = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio del armario.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Factor de capacidad
        precio *= self.calcular_factor_capacidad()
        
        # Premium por número de puertas
        precio += (self._numero_puertas * 100)
        
        # Premium por espejo
        if self._tiene_espejo:
            precio *= 1.15
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del armario.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Armario {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_almacenamiento() + "\n"
        descripcion += f"Puertas: {self._numero_puertas}\n"
        descripcion += f"Espejo: {'Sí' if self._tiene_espejo else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
