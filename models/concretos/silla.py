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
            tiene_respaldo: Si la silla tiene respaldo
            material_tapizado: Material del tapizado (opcional)
            altura_regulable: Si la silla puede regular su altura
            tiene_ruedas: Si la silla tiene ruedas
        """
        super().__init__(nombre, material, color, precio_base,
                         capacidad_personas=1, tiene_respaldo=tiene_respaldo,
                         material_tapizado=material_tapizado)
        self._altura_regulable = altura_regulable
        self._tiene_ruedas = tiene_ruedas
        self._altura_actual = 45  # altura estándar en cm

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
        precio *= self.calcular_factor_comodidad()
        if self._altura_regulable:
            precio *= 1.15
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

    def regular_altura(self, nueva_altura: int) -> str:
        """
        Simula la regulación de altura de la silla.

        Args:
            nueva_altura: Nueva altura en centímetros (30-70 cm)

        Returns:
            str: Mensaje del resultado de la operación
        """
        if not self._altura_regulable:
            return f"La silla {self.nombre} no tiene mecanismo de altura regulable"
        if nueva_altura < 30 or nueva_altura > 70:
            return "Altura inválida. Debe estar entre 30 y 70 cm"
        self._altura_actual = nueva_altura
        return f"Altura ajustada a {nueva_altura} cm correctamente"

    def es_silla_oficina(self) -> bool:
        """
        Determina si la silla es adecuada para oficina.
        Una silla es de oficina si tiene ruedas Y altura regulable.

        Returns:
            bool: True si es silla de oficina
        """
        return self._tiene_ruedas and self._altura_regulable
