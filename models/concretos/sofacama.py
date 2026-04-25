"""
Clase SofaCama que implementa herencia múltiple.
Esta clase hereda tanto de Sofa como de Cama.
"""

from .sofa import Sofa
from .cama import Cama


class SofaCama(Sofa, Cama):
    """
    Clase que implementa herencia múltiple heredando de Sofa y Cama.
    
    Un sofá-cama es un mueble que funciona tanto como asiento durante el día
    como cama durante la noche.
    
    Conceptos OOP aplicados:
    - Herencia múltiple: Hereda de Sofa y Cama
    - Resolución MRO: Maneja el orden de resolución de métodos
    - Polimorfismo: Implementa comportamientos únicos combinando funcionalidades
    - Super(): Usa super() para resolver conflictos de herencia
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 capacidad_personas: int = 3, material_tapizado: str = "tela",
                 tamaño_cama: str = "queen", incluye_colchon: bool = True,
                 mecanismo_conversion: str = "plegable"):
        """
        Constructor del sofá-cama.
        
        Args:
            capacidad_personas: Capacidad como sofá
            tamaño_cama: Tamaño cuando está desplegado como cama
            incluye_colchon: Si incluye colchón
            mecanismo_conversion: Tipo de mecanismo (plegable, corredizo, etc.)
        """
        # Inicializar Sofa (primer padre)
        Sofa.__init__(self, nombre, material, color, precio_base,
                     capacidad_personas=capacidad_personas,
                     material_tapizado=material_tapizado,
                     es_modular=False)
        
        # Inicializar atributos específicos de sofá-cama
        self._tamaño_cama = tamaño_cama
        self._incluye_colchon = incluye_colchon
        self._mecanismo_conversion = mecanismo_conversion
    
    @property
    def tamaño_cama(self) -> str:
        """Getter para el tamaño cuando es cama."""
        return self._tamaño_cama
    
    @property
    def incluye_colchon(self) -> bool:
        """Getter para si incluye colchón."""
        return self._incluye_colchon
    
    @property
    def mecanismo_conversion(self) -> str:
        """Getter para el tipo de mecanismo."""
        return self._mecanismo_conversion
    
    @tamaño_cama.setter
    def tamaño_cama(self, value: str) -> None:
        """Setter para tamaño de cama."""
        tamaños_validos = ["single", "double", "queen", "king"]
        if value.lower() not in tamaños_validos:
            raise ValueError(f"Tamaño debe ser uno de: {tamaños_validos}")
        self._tamaño_cama = value
    
    @incluye_colchon.setter
    def incluye_colchon(self, value: bool) -> None:
        """Setter para colchón."""
        self._incluye_colchon = value
    
    @mecanismo_conversion.setter
    def mecanismo_conversion(self, value: str) -> None:
        """Setter para mecanismo."""
        self._mecanismo_conversion = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio del sofá-cama.
        Combina características de sofá y cama.
        
        Returns:
            float: Precio calculado
        """
        # Usar el precio del sofá como base
        precio = self.precio_base
        
        # Factor de comodidad (del sofá)
        precio *= self.calcular_factor_comodidad()
        
        # Premium por capacidad como sofá
        precio *= (1.0 + (self.capacidad_personas - 1) * 0.2)
        
        # Premium por tamaño de cama
        tamaño_factor = {"single": 1.1, "double": 1.3, "queen": 1.5, "king": 1.7}
        precio *= tamaño_factor.get(self._tamaño_cama.lower(), 1.0)
        
        # Premium si incluye colchón
        if self._incluye_colchon:
            precio *= 1.3
        
        # Premium por mecanismo de conversión
        if self._mecanismo_conversion.lower() == "electrico":
            precio *= 1.4
        elif self._mecanismo_conversion.lower() == "corredizo":
            precio *= 1.2
        else:  # plegable
            precio *= 1.15
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa del sofá-cama.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Sofá-Cama {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += f"Capacidad (sofá): {self.capacidad_personas} personas\n"
        descripcion += f"Tamaño (cama): {self._tamaño_cama}\n"
        descripcion += self.obtener_info_asiento() + "\n"
        descripcion += f"Incluye colchón: {'Sí' if self._incluye_colchon else 'No'}\n"
        descripcion += f"Mecanismo: {self._mecanismo_conversion}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
        
        Args:
            mecanismo_conversion: Tipo de mecanismo de conversión (plegable, extensible, etc.)
            Otros argumentos se pasan a las clases padre
        """
        # TODO: Inicializar usando las clases padre
        # Nota: En herencia múltiple, solo se llama super().__init__ una vez
        # Esto llama al primer padre en el MRO (Method Resolution Order)
        # super().__init__(nombre, material, color, precio_base, capacidad_personas, True, material_tapizado)
        
        # TODO: Inicializar atributos específicos de cama
        # Necesitamos configurar manualmente los atributos de Cama ya que solo se llama un __init__
        # self._tamaño_cama = tamaño_cama
        # self._incluye_colchon = incluye_colchon
        
        # TODO: Inicializar atributos únicos del sofá-cama
        # self._mecanismo_conversion = mecanismo_conversion
        # self._modo_actual = "sofa"  # Puede ser "sofa" o "cama"
        pass
    
    # TODO: Implementar propiedades para los nuevos atributos
    # @property
    # def mecanismo_conversion(self) -> str:
    #     """Getter para el mecanismo de conversión."""
    #     return self._mecanismo_conversion
    
    # @property
    # def modo_actual(self) -> str:
    #     """Getter para el modo actual (sofa o cama)."""
    #     return self._modo_actual
    
    def convertir_a_cama(self) -> str:
        """
        Convierte el sofá en cama.
        Método específico del sofá-cama.
        
        Returns:
            str: Mensaje del resultado de la conversión
        """
        # TODO: Implementar lógica de conversión
        # if self._modo_actual == "cama":
        #     return "El sofá-cama ya está en modo cama"
        
        # self._modo_actual = "cama"
        # return f"Sofá convertido a cama usando mecanismo {self.mecanismo_conversion}"
        pass
    
    def convertir_a_sofa(self) -> str:
        """
        Convierte la cama en sofá.
        Método específico del sofá-cama.
        
        Returns:
            str: Mensaje del resultado de la conversión
        """
        # TODO: Implementar lógica de conversión
        # if self._modo_actual == "sofa":
        #     return "El sofá-cama ya está en modo sofá"
        
        # self._modo_actual = "sofa"
        # return f"Cama convertida a sofá usando mecanismo {self.mecanismo_conversion}"
        pass
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio combinando las funcionalidades de sofá y cama.
        
        Returns:
            float: Precio final del sofá-cama
        """
        # TODO: Implementar cálculo de precio combinado
        # El sofá-cama es más caro que un sofá o cama individual
        # 1. Comenzar con precio base
        # precio = self.precio_base
        
        # 2. Aplicar factor de comodidad de asiento
        # precio *= self.calcular_factor_comodidad()
        
        # 3. Agregar valor por funcionalidad dual
        # precio *= 1.5  # 50% más caro por ser dual
        
        # 4. Agregar costo por mecanismo de conversión
        # if self.mecanismo_conversion == "electrico":
        #     precio += 200
        # elif self.mecanismo_conversion == "hidraulico":
        #     precio += 150
        # else:  # manual/plegable
        #     precio += 100
        
        # 5. Agregar costo si incluye colchón
        # if self.incluye_colchon:
        #     precio += 300
        
        # return round(precio, 2)
        pass
    
    def obtener_descripcion(self) -> str:
        """
        Descripción que combina características de sofá y cama.
        
        Returns:
            str: Descripción completa del sofá-cama
        """
        # TODO: Crear descripción combinada
        # descripcion = f"Sofá-cama {self.nombre} fabricado en {self.material} color {self.color}."
        # descripcion += f"\n{self.obtener_info_asiento()}"
        # descripcion += f"\nTamaño de cama: {self.tamaño_cama}"
        # descripcion += f"\nMecanismo de conversión: {self.mecanismo_conversion}"
        # descripcion += f"\nColchón incluido: {'Sí' if self.incluye_colchon else 'No'}"
        # descripcion += f"\nModo actual: {self.modo_actual}"
        # descripcion += f"\nPrecio: ${self.calcular_precio():.2f}"
        # return descripcion
        pass
    
    def obtener_capacidad_total(self) -> dict:
        """
        Obtiene la capacidad tanto como sofá como cama.
        Método único del sofá-cama.
        
        Returns:
            dict: Capacidades en ambos modos
        """
        # TODO: Implementar capacidades
        # capacidades = {
        #     "como_sofa": self.capacidad_personas,
        #     "como_cama": 2 if self.tamaño_cama in ["matrimonial", "queen", "king"] else 1
        # }
        # return capacidades
        pass
    
    # TODO: Implementar método para verificar compatibilidad de modo
    # def puede_usar_como_cama(self) -> bool:
    #     """Verifica si actualmente puede usarse como cama."""
    #     return self._modo_actual == "cama"
    
    # def puede_usar_como_sofa(self) -> bool:
    #     """Verifica si actualmente puede usarse como sofá."""
    #     return self._modo_actual == "sofa"
    
    def __str__(self) -> str:
        """
        Representación en cadena del sofá-cama.
        Sobrescribe el método heredado para mostrar información específica.
        """
        # TODO: Implementar representación personalizada
        # return f"Sofá-cama {self.nombre} (modo: {self.modo_actual})"
        pass

