"""
Clase abstracta para muebles de almacenamiento.
Agrupa características comunes de armarios, cajoneras y similares.
"""

from abc import abstractmethod
from ..mueble import Mueble


class Almacenamiento(Mueble):
    """
    Clase abstracta para muebles de almacenamiento.
    
    Define las características comunes de muebles diseñados para guardar
    objetos, como armarios, cajoneras, estanterías, etc.
    
    Conceptos OOP aplicados:
    - Herencia: Extiende la clase Mueble
    - Abstracción: Agrupa características comunes de almacenamiento
    - Polimorfismo: Permite diferentes cálculos de precio según tipo
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_volumen: float, numero_compartimientos: int, tiene_cerraduras: bool = False):
        """
        Constructor para muebles de almacenamiento.
        
        Args:
            capacidad_volumen: Volumen de almacenamiento en metros cúbicos
            numero_compartimientos: Número de divisiones o compartimientos
            tiene_cerraduras: Si tiene cerraduras de seguridad
            Otros argumentos heredados de Mueble
        """
        super().__init__(nombre, material, color, precio_base)
        
        self._capacidad_volumen = capacidad_volumen
        self._numero_compartimientos = numero_compartimientos
        self._tiene_cerraduras = tiene_cerraduras
    
    # Propiedades (getters)
    @property
    def capacidad_volumen(self) -> float:
        """Getter para la capacidad de volumen."""
        return self._capacidad_volumen
    
    @property
    def numero_compartimientos(self) -> int:
        """Getter para el número de compartimientos."""
        return self._numero_compartimientos
    
    @property
    def tiene_cerraduras(self) -> bool:
        """Getter para si tiene cerraduras."""
        return self._tiene_cerraduras
    
    # Setters con validaciones
    @capacidad_volumen.setter
    def capacidad_volumen(self, value: float) -> None:
        """Setter para capacidad de volumen con validación."""
        if value <= 0:
            raise ValueError("La capacidad de volumen debe ser mayor a 0")
        self._capacidad_volumen = value
    
    @numero_compartimientos.setter
    def numero_compartimientos(self, value: int) -> None:
        """Setter para número de compartimientos con validación."""
        if value <= 0:
            raise ValueError("Debe haber al menos 1 compartimiento")
        self._numero_compartimientos = value
    
    @tiene_cerraduras.setter
    def tiene_cerraduras(self, value: bool) -> None:
        """Setter para cerraduras."""
        self._tiene_cerraduras = value
    
    def calcular_factor_capacidad(self) -> float:
        """
        Calcula un factor de capacidad basado en el volumen y compartimientos.
        
        Returns:
            float: Factor multiplicador para el precio
        """
        # Base de 1.0 por capacidad
        factor = 1.0 + (self._capacidad_volumen * 0.1)
        
        # Bonus por compartimientos
        if self._numero_compartimientos > 3:
            factor += 0.15
        
        # Bonus por cerraduras
        if self._tiene_cerraduras:
            factor += 0.2
        
        return factor
    
    def obtener_info_almacenamiento(self) -> str:
        """
        Obtiene información del mueble de almacenamiento.
        
        Returns:
            str: Información detallada
        """
        info = f"Volumen: {self.capacidad_volumen} m³"
        info += f", Compartimientos: {self.numero_compartimientos}"
        info += f", Cerraduras: {'Sí' if self.tiene_cerraduras else 'No'}"
        return info
