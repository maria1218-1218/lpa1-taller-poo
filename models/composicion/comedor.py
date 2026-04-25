"""
Clase Comedor que implementa composición.
Un comedor está compuesto por una mesa y varias sillas.
"""

from typing import List
from ..concretos.mesa import Mesa
from ..concretos.silla import Silla


class Comedor:
    """
    Clase que implementa composición conteniendo una mesa y sillas.
    
    Un comedor es un conjunto de muebles que trabajan juntos.
    La relación es de composición porque el comedor "tiene" una mesa
    y "tiene" sillas, pero estas pueden existir independientemente.
    
    Conceptos OOP aplicados:
    - Composición: El comedor contiene otros objetos (mesa y sillas)
    - Agregación: Los objetos contenidos pueden existir independientemente
    - Encapsulación: Controla el acceso a los componentes internos
    - Abstracción: Simplifica la gestión de múltiples muebles
    """
    
    def __init__(self, nombre: str, mesa: Mesa, sillas: List[Silla] = None):
        """
        Constructor del comedor.
        
        Args:
            nombre: Nombre del set de comedor
            mesa: Objeto Mesa que forma parte del comedor
            sillas: Lista de objetos Silla (opcional, se puede crear vacía)
        """
        self._nombre = nombre
        self._mesa = mesa
        self._sillas = sillas if sillas is not None else []
    
    # Implementar propiedades
    @property
    def nombre(self) -> str:
        """Getter para el nombre del comedor."""
        return self._nombre
    
    @property
    def mesa(self) -> Mesa:
        """Getter para la mesa del comedor."""
        return self._mesa
    
    @property
    def sillas(self) -> List[Silla]:
        """Getter para la lista de sillas."""
        return self._sillas.copy()
    
    @property
    def numero_sillas(self) -> int:
        """Getter para el número de sillas."""
        return len(self._sillas)
    
    # Setters
    @nombre.setter
    def nombre(self, value: str) -> None:
        """Setter para el nombre."""
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip()
    
    @mesa.setter
    def mesa(self, value: Mesa) -> None:
        """Setter para la mesa."""
        if not isinstance(value, Mesa):
            raise TypeError("Debe ser una instancia de Mesa")
        self._mesa = value
    
    # Métodos de gestión de sillas
    def agregar_silla(self, silla: Silla) -> None:
        """
        Agrega una silla al comedor.
        
        Args:
            silla: Objeto Silla a agregar
        """
        if not isinstance(silla, Silla):
            raise TypeError("Debe ser una instancia de Silla")
        self._sillas.append(silla)
    
    def agregar_sillas(self, sillas: List[Silla]) -> None:
        """
        Agrega múltiples sillas al comedor.
        
        Args:
            sillas: Lista de objetos Silla
        """
        for silla in sillas:
            self.agregar_silla(silla)
    
    def quitar_silla(self, indice: int) -> Silla:
        """
        Quita una silla del comedor por índice.
        
        Args:
            indice: Índice de la silla a quitar
            
        Returns:
            Silla: La silla removida
        """
        if indice < 0 or indice >= len(self._sillas):
            raise IndexError("Índice de silla inválido")
        return self._sillas.pop(indice)
    
    def limpiar_sillas(self) -> None:
        """Quita todas las sillas del comedor."""
        self._sillas.clear()
    
    def calcular_precio_total(self) -> float:
        """
        Calcula el precio total del comedor (mesa + sillas).
        
        Returns:
            float: Precio total
        """
        precio = self._mesa.calcular_precio()
        for silla in self._sillas:
            precio += silla.calcular_precio()
        return round(precio, 2)
    
    def obtener_info_comedor(self) -> str:
        """
        Obtiene información detallada del comedor.
        
        Returns:
            str: Información del comedor
        """
        info = f"Comedor: {self._nombre}\n"
        info += f"Mesa: {self._mesa.nombre} - ${self._mesa.calcular_precio()}\n"
        info += f"Número de sillas: {len(self._sillas)}\n"
        
        for i, silla in enumerate(self._sillas, 1):
            info += f"  Silla {i}: {silla.nombre} - ${silla.calcular_precio()}\n"
        
        info += f"Precio total: ${self.calcular_precio_total()}"
        return info
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del comedor.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"SET COMEDOR: {self._nombre}\n"
        descripcion += "=" * 50 + "\n\n"
        
        descripcion += "MESA:\n"
        descripcion += self._mesa.obtener_descripcion() + "\n\n"
        
        descripcion += f"SILLAS ({len(self._sillas)} total):\n"
        for i, silla in enumerate(self._sillas, 1):
            descripcion += f"\nSilla {i}:\n"
            descripcion += silla.obtener_descripcion() + "\n"
        
        descripcion += "\n" + "=" * 50 + "\n"
        descripcion += f"PRECIO TOTAL DEL SET: ${self.calcular_precio_total()}"
        
        return descripcion
    #     return self._mesa
    
    # @property
    # def sillas(self) -> List['Silla']:
    #     """Getter para la lista de sillas."""
    #     return self._sillas.copy()  # Retorna una copia para proteger la lista interna
    
    def agregar_silla(self, silla: 'Silla') -> str:
        """
        Agrega una silla al comedor.
        
        Args:
            silla: Objeto Silla a agregar
            
        Returns:
            str: Mensaje de confirmación
        """
        # TODO: Implementar lógica para agregar silla
        # Validar que sea realmente una Silla
        # if not isinstance(silla, Silla):
        #     return "Error: Solo se pueden agregar objetos de tipo Silla"
        
        # Verificar capacidad máxima (por ejemplo, basada en el tamaño de la mesa)
        # capacidad_maxima = self._calcular_capacidad_maxima()
        # if len(self._sillas) >= capacidad_maxima:
        #     return f"No se pueden agregar más sillas. Capacidad máxima: {capacidad_maxima}"
        
        # self._sillas.append(silla)
        # return f"Silla {silla.nombre} agregada exitosamente al comedor"
        pass
    
    def quitar_silla(self, indice: int = -1) -> str:
        """
        Quita una silla del comedor.
        
        Args:
            indice: Índice de la silla a quitar (-1 para la última)
            
        Returns:
            str: Mensaje de confirmación
        """
        # TODO: Implementar lógica para quitar silla
        # if not self._sillas:
        #     return "No hay sillas para quitar"
        
        # try:
        #     silla_removida = self._sillas.pop(indice)
        #     return f"Silla {silla_removida.nombre} removida del comedor"
        # except IndexError:
        #     return "Índice de silla inválido"
        pass
    
    def calcular_precio_total(self) -> float:
        """
        Calcula el precio total del comedor sumando todos sus componentes.
        
        Returns:
            float: Precio total del set de comedor
        """
        # TODO: Implementar cálculo de precio total
        # precio_total = self._mesa.calcular_precio()
        
        # for silla in self._sillas:
        #     precio_total += silla.calcular_precio()
        
        # # Aplicar descuento por set completo (5% si tiene 4 o más sillas)
        # if len(self._sillas) >= 4:
        #     precio_total *= 0.95  # 5% de descuento
        
        # return round(precio_total, 2)
        pass
    
    def obtener_descripcion_completa(self) -> str:
        """
        Obtiene una descripción completa del comedor y todos sus componentes.
        
        Returns:
            str: Descripción detallada del comedor
        """
        # TODO: Implementar descripción completa
        # descripcion = f"=== COMEDOR {self.nombre.upper()} ===\n\n"
        # descripcion += "MESA:\n"
        # descripcion += self._mesa.obtener_descripcion() + "\n\n"
        
        # if self._sillas:
        #     descripcion += f"SILLAS ({len(self._sillas)} unidades):\n"
        #     for i, silla in enumerate(self._sillas, 1):
        #         descripcion += f"{i}. {silla.obtener_descripcion()}\n"
        # else:
        #     descripcion += "SILLAS: Ninguna incluida\n"
        
        # descripcion += f"\n--- PRECIO TOTAL: ${self.calcular_precio_total():.2f} ---"
        # if len(self._sillas) >= 4:
        #     descripcion += "\n(Incluye 5% de descuento por set completo)"
        
        # return descripcion
        pass
    
    def _calcular_capacidad_maxima(self) -> int:
        """
        Calcula la capacidad máxima de sillas basada en el tamaño de la mesa.
        Método privado auxiliar.
        
        Returns:
            int: Número máximo de sillas que pueden acomodarse
        """
        # TODO: Implementar cálculo de capacidad
        # Este cálculo depende del tamaño de la mesa
        # Asumir que la mesa tiene un atributo como 'capacidad_personas' o 'forma'
        
        # Ejemplo de lógica:
        # if hasattr(self._mesa, 'capacidad_personas'):
        #     return self._mesa.capacidad_personas
        # else:
        #     # Capacidad por defecto basada en el tamaño
        #     return 6  # Valor por defecto
        
        return 6  # Valor temporal
    
    def obtener_resumen(self) -> dict:
        """
        Obtiene un resumen estadístico del comedor.
        
        Returns:
            dict: Diccionario con información resumida
        """
        # TODO: Implementar resumen estadístico
        # resumen = {
        #     "nombre": self.nombre,
        #     "total_muebles": 1 + len(self._sillas),  # mesa + sillas
        #     "precio_mesa": self._mesa.calcular_precio(),
        #     "precio_sillas": sum(silla.calcular_precio() for silla in self._sillas),
        #     "precio_total": self.calcular_precio_total(),
        #     "capacidad_personas": len(self._sillas),
        #     "materiales_utilizados": self._obtener_materiales_unicos()
        # }
        # return resumen
        pass
    
    def _obtener_materiales_unicos(self) -> list:
        """
        Obtiene una lista de materiales únicos usados en el comedor.
        Método privado auxiliar.
        
        Returns:
            list: Lista de materiales únicos
        """
        # TODO: Implementar obtención de materiales
        # materiales = {self._mesa.material}  # Usar set para evitar duplicados
        # 
        # for silla in self._sillas:
        #     materiales.add(silla.material)
        #     if hasattr(silla, 'material_tapizado') and silla.material_tapizado:
        #         materiales.add(silla.material_tapizado)
        # 
        # return list(materiales)
        pass
    
    def __str__(self) -> str:
        """Representación en cadena del comedor."""
        # TODO: Implementar representación
        # return f"Comedor {self.nombre}: Mesa + {len(self._sillas)} sillas"
        pass
    
    def __len__(self) -> int:
        """Retorna el número total de muebles en el comedor."""
        # TODO: Implementar longitud
        # return 1 + len(self._sillas)  # mesa + sillas
        pass

