"""
Clase concreta Cajonera.
Mueble de almacenamiento con cajones.
"""

from ..categorias.almacenamiento import Almacenamiento


class Cajonera(Almacenamiento):
    """
    Clase concreta que representa una cajonera.
    
    Una cajonera es un mueble de almacenamiento compuesto principalmente
    de cajones para guardar diversos objetos.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_volumen: float, numero_compartimientos: int,
                 profundidad_cajones: float = 50.0, deslizable: bool = True):
        """
        Constructor de la cajonera.
        
        Args:
            profundidad_cajones: Profundidad de los cajones en cm
            deslizable: Si los cajones son deslizables (correderas de calidad)
        """
        super().__init__(nombre, material, color, precio_base,
                        capacidad_volumen, numero_compartimientos,
                        tiene_cerraduras=False)
        
        self._profundidad_cajones = profundidad_cajones
        self._deslizable = deslizable
    
    @property
    def profundidad_cajones(self) -> float:
        """Getter para profundidad de cajones."""
        return self._profundidad_cajones
    
    @property
    def deslizable(self) -> bool:
        """Getter para si es deslizable."""
        return self._deslizable
    
    @profundidad_cajones.setter
    def profundidad_cajones(self, value: float) -> None:
        """Setter para profundidad."""
        if value <= 0:
            raise ValueError("La profundidad debe ser mayor a 0")
        self._profundidad_cajones = value
    
    @deslizable.setter
    def deslizable(self, value: bool) -> None:
        """Setter para deslizable."""
        self._deslizable = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio de la cajonera.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Factor de capacidad
        precio *= self.calcular_factor_capacidad()
        
        # Premium por profundidad
        precio *= (1.0 + (self._profundidad_cajones / 100 * 0.1))
        
        # Premium por deslizable
        if self._deslizable:
            precio *= 1.25
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa de la cajonera.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Cajonera {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_almacenamiento() + "\n"
        descripcion += f"Profundidad de cajones: {self._profundidad_cajones} cm\n"
        descripcion += f"Deslizable: {'Sí' if self._deslizable else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
