"""
Clase concreta Silla.
Implementa un mueble de asiento específico para una persona.
"""

from ..categorias.asientos import Asiento


class Silla(Asiento):
    """
    Clase concreta que representa una silla.
    
    Una silla es un asiento individual con características específicas
    como altura regulable, ruedas, etc.
    
    Conceptos OOP aplicados:
    - Herencia: Hereda de Asiento
    - Polimorfismo: Implementa métodos abstractos de manera específica
    - Encapsulación: Protege atributos específicos de la silla
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 tiene_respaldo: bool = True, material_tapizado: str = None,
                 altura_regulable: bool = False, tiene_ruedas: bool = False):
        """
        Constructor de la silla.
        
        Args:
            altura_regulable: Si la silla puede regular su altura
            tiene_ruedas: Si la silla tiene ruedas
            Otros argumentos heredados de Asiento
        """
        # Llamar al constructor padre con capacidad fija de 1 persona
        super().__init__(nombre, material, color, precio_base, 
                        capacidad_personas=1, tiene_respaldo=tiene_respaldo,
                        material_tapizado=material_tapizado)
        
        # Inicializar atributos específicos de la silla
        self._altura_regulable = altura_regulable
        self._tiene_ruedas = tiene_ruedas
    
    # Implementar propiedades para los nuevos atributos
    @property
    def altura_regulable(self) -> bool:
        """Getter para altura regulable."""
        return self._altura_regulable
    
    @property
    def tiene_ruedas(self) -> bool:
        """Getter para si tiene ruedas."""
        return self._tiene_ruedas
    
    @altura_regulable.setter
    def altura_regulable(self, value: bool) -> None:
        """Setter para altura regulable."""
        self._altura_regulable = value
    
    @tiene_ruedas.setter
    def tiene_ruedas(self, value: bool) -> None:
        """Setter para ruedas."""
        self._tiene_ruedas = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio final de la silla.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Aplicar factor de comodidad
        precio *= self.calcular_factor_comodidad()
        
        # Agregar costo por altura regulable
        if self._altura_regulable:
            precio *= 1.15
        
        # Agregar costo por ruedas
        if self._tiene_ruedas:
            precio *= 1.2
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa de la silla.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Silla {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_asiento() + "\n"
        descripcion += f"Altura regulable: {'Sí' if self._altura_regulable else 'No'}\n"
        descripcion += f"Con ruedas: {'Sí' if self._tiene_ruedas else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
    
    def calcular_precio(self) -> float:
        """
        Implementa el cálculo de precio específico para sillas.
        
        Returns:
            float: Precio final de la silla
        """
        # TODO: Implementar cálculo de precio para silla

        # 1. Comenzar con el precio base
        
        # 2. Aplicar factor de comodidad heredado
        
        # 3. Agregar costos por características especiales
        
        # 4. Retornar precio redondeado a 2 decimales

        pass
    
    def obtener_descripcion(self) -> str:
        """
        Implementa la descripción específica de la silla.
        
        Returns:
            str: Descripción completa de la silla
        """
        # TODO: Crear y retornar descripción detallada
        
        pass
    
    def regular_altura(self, nueva_altura: int) -> str:
        """
        Simula la regulación de altura de la silla.
        Método específico de la clase Silla.
        
        Args:
            nueva_altura: Nueva altura en centímetros
            
        Returns:
            str: Mensaje del resultado de la operación
        """
        # TODO: Implementar lógica de regulación

        pass
    
    def es_silla_oficina(self) -> bool:
        """
        Determina si la silla es adecuada para oficina.
        
        Returns:
            bool: True si es silla de oficina
        """
        # TODO: Una silla es de oficina si tiene ruedas Y altura regulable

        pass

