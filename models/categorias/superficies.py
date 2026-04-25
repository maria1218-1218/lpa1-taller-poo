"""
Clase abstracta para muebles para superficies de trabajo o del hogar.
Agrupa características comunes de mesas, escritorios y similares.
"""

from abc import abstractmethod
from ..mueble import Mueble


class Superficie(Mueble):
    """
    Clase abstracta para muebles que proporcionan superficies.
    
    Define las características comunes de muebles diseñados para proporcionar
    superficies de trabajo o del hogar, como mesas, escritorios, mostradores, etc.
    
    Conceptos OOP aplicados:
    - Herencia: Extiende la clase Mueble
    - Abstracción: Agrupa características comunes de superficies
    - Polimorfismo: Diferentes tipos de superficies con diferentes características
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 largo: float, ancho: float, alto: float, material_superficie: str):
        """
        Constructor para muebles de superficie.
        
        Args:
            largo: Largo de la superficie en centímetros
            ancho: Ancho de la superficie en centímetros
            alto: Alto del mueble en centímetros
            material_superficie: Material de la superficie (madera, vidrio, mármol, etc.)
            Otros argumentos heredados de Mueble
        """
        super().__init__(nombre, material, color, precio_base)
        
        self._largo = largo
        self._ancho = ancho
        self._alto = alto
        self._material_superficie = material_superficie
    
    # Propiedades (getters)
    @property
    def largo(self) -> float:
        """Getter para el largo."""
        return self._largo
    
    @property
    def ancho(self) -> float:
        """Getter para el ancho."""
        return self._ancho
    
    @property
    def alto(self) -> float:
        """Getter para el alto."""
        return self._alto
    
    @property
    def material_superficie(self) -> str:
        """Getter para el material de la superficie."""
        return self._material_superficie
    
    # Setters con validaciones
    @largo.setter
    def largo(self, value: float) -> None:
        """Setter para largo con validación."""
        if value <= 0:
            raise ValueError("El largo debe ser mayor a 0")
        self._largo = value
    
    @ancho.setter
    def ancho(self, value: float) -> None:
        """Setter para ancho con validación."""
        if value <= 0:
            raise ValueError("El ancho debe ser mayor a 0")
        self._ancho = value
    
    @alto.setter
    def alto(self, value: float) -> None:
        """Setter para alto con validación."""
        if value <= 0:
            raise ValueError("El alto debe ser mayor a 0")
        self._alto = value
    
    @material_superficie.setter
    def material_superficie(self, value: str) -> None:
        """Setter para material de la superficie."""
        if not value or not value.strip():
            raise ValueError("El material de la superficie no puede estar vacío")
        self._material_superficie = value.strip()
    
    def calcular_area_superficie(self) -> float:
        """
        Calcula el área de la superficie en centímetros cuadrados.
        
        Returns:
            float: Área en cm²
        """
        return self._largo * self._ancho
    
    def calcular_factor_material_superficie(self) -> float:
        """
        Calcula un factor de precio basado en el material de la superficie.
        
        Returns:
            float: Factor multiplicador
        """
        material = self._material_superficie.lower()
        
        if material == "vidrio":
            return 1.3
        elif material == "mármol":
            return 1.5
        elif material == "granito":
            return 1.4
        elif material == "madera":
            return 1.0
        elif material == "fórmica":
            return 0.9
        else:
            return 1.0
    
    def obtener_info_superficie(self) -> str:
        """
        Obtiene información del mueble de superficie.
        
        Returns:
            str: Información detallada
        """
        area = self.calcular_area_superficie()
        info = f"Dimensiones: {self.largo}x{self.ancho}x{self.alto} cm"
        info += f", Área: {area} cm²"
        info += f", Superficie: {self.material_superficie}"
        return info
