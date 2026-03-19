from abc import ABC, abstractmethod
"""
Clase base abstracta Mueble
Este es el punto de partida de nuestra jerarquía de clases.
"""

# Importar ABC y abstractmethod del módulo abc
# Estos son necesarios para crear clases y métodos abstractos


class Mueble(ABC):
    """
    Clase abstracta base para todos los muebles.
    
    Esta clase define la estructura común que deben tener todos los muebles
    de nuestra tienda, pero no puede ser instanciada directamente.
    
    Conceptos OOP aplicados:
    - Abstracción: Define una interfaz común sin implementación específica
    - Encapsulación: Usa atributos privados con getters/setters
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float):
        """
        Constructor de la clase Mueble.
        
        Args:
            nombre: Nombre del mueble
            material: Material principal (madera, metal, plástico, etc.)
            color: Color del mueble
            precio_base: Precio base antes de aplicar modificadores
        """
        # Inicializar los atributos privados usando underscore
        # Ejemplo: self._nombre = nombre
        self._nombre = nombre 
        self._material = material 
        self._color = color
        self._precio_base = precio_base
        # Esto implementa encapsulación, ocultando los datos internos
        pass
    
    # Implementar las propiedades (getters) para cada atributo
    # Usa el decorador @property para crear getters
    # Ejemplo:
    @property
    def nombre(self) -> str:
        """Getter para el nombre del mueble."""
        return self._nombre
    
    @property
    def material(self) -> str:
        """Getter para el material."""
        return self._material 

    @property
    def color(self) -> str:
        """Getter para el color."""
        return self._color 

    @property
    def precio_base(self) -> str:
        """Getter para el precio base."""
        return self._precio_base

        
    # Implementar los setters para cada atributo donde sea necesario
    # Usa el decorador @nombre.setter para crear setters
    # Incluye validaciones básicas (ej: precio no puede ser negativo)
    # Ejemplo:
    @nombre.setter
    def nombre(self, value: str) -> None:
        """Setter para el nombre con validación."""
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip()
    
    # Implementar método abstracto calcular_precio()
    # Este método debe ser implementado por todas las clases hijas
    # Usa el decorador @abstractmethod
    @abstractmethod
    def calcular_precio(self) -> float:
        """
        Calcula el precio final del mueble.
        Este método debe ser implementado por cada clase concreta.
        
        Returns:
            float: Precio final calculado
        """
        pass
    
    # Implementar método abstracto obtener_descripcion()
    # Este método debe retornar una descripción detallada del mueble
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción detallada del mueble.
        Este método debe ser implementado por cada clase concreta.
        
        Returns:
            str: Descripción completa del mueble
        """
        pass
    
    def __str__(self) -> str:
        """
        Representación en cadena del mueble.
        Este método concreto puede ser usado por todas las clases hijas.
        """
        # Implementar usando las propiedades
        return f"{self.nombre} de {self.material} en color {self.color}"
        pass
    
    def __repr__(self) -> str:
        """
        Representación técnica del mueble para debugging.
        """
        # Implementar una representación técnica
        return f"Mueble(nombre='{self.nombre}', material='{self.material}', color='{self.color}', precio_base={self.precio_base})"
        pass

