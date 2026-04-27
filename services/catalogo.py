"""
Clase Catalogo para gestionar el catálogo de muebles por categorías.
"""

from typing import List, Dict
from models.mueble import Mueble


class Catalogo:
    """
    Gestiona el catálogo de muebles organizados por categorías.

    Conceptos OOP aplicados:
    - Encapsulación: Agrupa la lógica de gestión del catálogo
    - Composición: Contiene colecciones de Mueble agrupadas por categoría
    """

    def __init__(self, nombre: str = "Catálogo General"):
        self._nombre = nombre
        self._items: Dict[str, List[Mueble]] = {}

    @property
    def nombre(self) -> str:
        """Getter para el nombre del catálogo."""
        return self._nombre

    def agregar_item(self, mueble: Mueble, categoria: str = "General") -> None:
        """
        Agrega un mueble al catálogo en la categoría indicada.

        Args:
            mueble: Objeto Mueble a agregar
            categoria: Categoría donde clasificar el mueble
        """
        if not isinstance(mueble, Mueble):
            raise TypeError("Solo se pueden agregar objetos de tipo Mueble")
        categoria = categoria.strip()
        if categoria not in self._items:
            self._items[categoria] = []
        self._items[categoria].append(mueble)

    def obtener_por_categoria(self, categoria: str) -> List[Mueble]:
        """
        Devuelve todos los muebles de una categoría.

        Args:
            categoria: Nombre de la categoría

        Returns:
            List[Mueble]: Lista de muebles de esa categoría
        """
        return list(self._items.get(categoria.strip(), []))

    def listar_categorias(self) -> List[str]:
        """Devuelve los nombres de todas las categorías."""
        return list(self._items.keys())

    def buscar_por_nombre(self, nombre: str) -> List[Mueble]:
        """
        Busca muebles por nombre en todas las categorías (case-insensitive).

        Returns:
            List[Mueble]: Muebles cuyo nombre contiene el término buscado
        """
        nombre_lower = nombre.lower()
        resultados = []
        for items in self._items.values():
            for item in items:
                if nombre_lower in item.nombre.lower():
                    resultados.append(item)
        return resultados

    def obtener_todos(self) -> List[Mueble]:
        """Devuelve todos los muebles del catálogo."""
        todos: List[Mueble] = []
        for items in self._items.values():
            todos.extend(items)
        return todos

    def total_items(self) -> int:
        """Retorna el número total de muebles en el catálogo."""
        return sum(len(items) for items in self._items.values())

    def calcular_valor_total(self) -> float:
        """Calcula el valor total de todos los muebles en el catálogo."""
        total = 0.0
        for items in self._items.values():
            for item in items:
                try:
                    total += item.calcular_precio()
                except Exception:
                    continue
        return round(total, 2)

    def generar_catalogo_texto(self) -> str:
        """
        Genera una representación en texto del catálogo completo.

        Returns:
            str: Catálogo formateado
        """
        if self.total_items() == 0:
            return f"Catálogo '{self._nombre}' está vacío"
        texto = f"=== {self._nombre.upper()} ===\n\n"
        for categoria, items in self._items.items():
            texto += f"--- {categoria} ---\n"
            for i, item in enumerate(items, 1):
                try:
                    precio = item.calcular_precio()
                    texto += f"  {i}. {item.nombre} ({item.material}, {item.color}) - ${precio:.2f}\n"
                except Exception:
                    texto += f"  {i}. {item.nombre} - Error al calcular precio\n"
            texto += "\n"
        texto += f"Total: {self.total_items()} items | Valor: ${self.calcular_valor_total():.2f}"
        return texto

    def __str__(self) -> str:
        return f"Catálogo '{self._nombre}': {self.total_items()} items en {len(self._items)} categorías"

    def __len__(self) -> int:
        return self.total_items()
