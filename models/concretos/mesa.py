"""
Clase concreta Mesa.
Una superficie de trabajo para comer o trabajar.
"""

from ..categorias.superficies import Superficie


class Mesa(Superficie):
    """
    Clase concreta que representa una mesa.
    
    Una mesa es una superficie de trabajo típicamente usada para comer,
    trabajar o colocar objetos.
    """
    
    def __init__(self, nombre: str, material: str, color: str, precio_base: float,
                 largo: float, ancho: float, alto: float, material_superficie: str,
                 numero_patas: int = 4, plegable: bool = False):
        """
        Constructor de la mesa.
        
        Args:
            numero_patas: Número de patas de la mesa
            plegable: Si la mesa es plegable
        """
        super().__init__(nombre, material, color, precio_base,
                        largo, ancho, alto, material_superficie)
        
        self._numero_patas = numero_patas
        self._plegable = plegable
    
    @property
    def numero_patas(self) -> int:
        """Getter para número de patas."""
        return self._numero_patas
    
    @property
    def plegable(self) -> bool:
        """Getter para si es plegable."""
        return self._plegable
    
    @numero_patas.setter
    def numero_patas(self, value: int) -> None:
        """Setter para número de patas."""
        if value < 1:
            raise ValueError("Debe haber al menos 1 pata")
        self._numero_patas = value
    
    @plegable.setter
    def plegable(self, value: bool) -> None:
        """Setter para plegable."""
        self._plegable = value
    
    def calcular_precio(self) -> float:
        """
        Calcula el precio de la mesa.
        
        Returns:
            float: Precio calculado
        """
        precio = self.precio_base
        
        # Factor por área de la superficie
        area = self.calcular_area_superficie()
        precio *= (1.0 + (area / 1000 * 0.1))
        
        # Factor por material de la superficie
        precio *= self.calcular_factor_material_superficie()
        
        # Premium por número de patas
        if self._numero_patas > 4:
            precio *= 1.1
        
        # Descuento si es plegable
        if self._plegable:
            precio *= 0.85
        
        return round(precio, 2)
    
    def obtener_descripcion(self) -> str:
        """
        Obtiene una descripción completa de la mesa.
        
        Returns:
            str: Descripción detallada
        """
        descripcion = f"Mesa {self.nombre}\n"
        descripcion += f"Material: {self.material}\n"
        descripcion += f"Color: {self.color}\n"
        descripcion += self.obtener_info_superficie() + "\n"
        descripcion += f"Patas: {self._numero_patas}\n"
        descripcion += f"Plegable: {'Sí' if self._plegable else 'No'}\n"
        descripcion += f"Precio: ${self.calcular_precio()}"
        return descripcion
