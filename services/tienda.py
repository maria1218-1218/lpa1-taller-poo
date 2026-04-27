"""
Servicio de la tienda que maneja la lógica de negocio.
"""

from typing import List, Dict, Optional
from models.mueble import Mueble
from models.composicion.comedor import Comedor


class TiendaMuebles:
    """
    Clase que maneja toda la lógica de negocio de la tienda de muebles.

    Conceptos OOP aplicados:
    - Encapsulación: Agrupa toda la lógica relacionada con la tienda
    - Abstracción: Oculta la complejidad del manejo de inventario
    - Composición: Contiene colecciones de muebles
    """

    def __init__(self, nombre_tienda: str = "Mueblería OOP"):
        self._nombre = nombre_tienda
        self._inventario: List[Mueble] = []
        self._comedores: List[Comedor] = []
        self._ventas_realizadas: List[Dict] = []
        self._descuentos_activos: Dict[str, float] = {}

    @property
    def nombre(self) -> str:
        """Getter para el nombre de la tienda."""
        return self._nombre

    @property
    def total_muebles(self) -> int:
        """Total de muebles en inventario."""
        return len(self._inventario)

    @property
    def total_comedores(self) -> int:
        """Total de comedores en la tienda."""
        return len(self._comedores)

    @property
    def total_ventas(self) -> int:
        """Total de ventas realizadas."""
        return len(self._ventas_realizadas)

    def agregar_mueble(self, mueble: Mueble) -> str:
        """
        Agrega un mueble al inventario.

        Returns:
            str: Mensaje de confirmación o error
        """
        if not isinstance(mueble, Mueble):
            return "Error: Solo se pueden agregar objetos de tipo Mueble"
        try:
            precio = mueble.calcular_precio()
            if precio <= 0:
                return "Error: El mueble debe tener un precio válido mayor a 0"
        except Exception as e:
            return f"Error al calcular precio del mueble: {str(e)}"
        self._inventario.append(mueble)
        return f"✓ Mueble '{mueble.nombre}' agregado exitosamente al inventario"

    def agregar_comedor(self, comedor: Comedor) -> str:
        """
        Agrega un comedor completo a la tienda.

        Returns:
            str: Mensaje de confirmación
        """
        if not isinstance(comedor, Comedor):
            return "Error: Solo se pueden agregar objetos de tipo Comedor"
        self._comedores.append(comedor)
        return f"✓ Comedor '{comedor.nombre}' agregado exitosamente"

    def eliminar_mueble(self, indice: int) -> str:
        """Elimina un mueble del inventario por índice."""
        if indice < 0 or indice >= len(self._inventario):
            return "Error: Índice de mueble inválido"
        mueble = self._inventario.pop(indice)
        return f"✓ Mueble '{mueble.nombre}' eliminado del inventario"

    def buscar_muebles_por_nombre(self, nombre: str) -> List[Mueble]:
        """Busca muebles por nombre (búsqueda parcial, case-insensitive)."""
        if not nombre or not nombre.strip():
            return []
        nombre_lower = nombre.lower().strip()
        return [m for m in self._inventario if nombre_lower in m.nombre.lower()]

    def filtrar_por_precio(self, precio_min: float = 0,
                           precio_max: float = float('inf')) -> List[Mueble]:
        """Filtra muebles por rango de precios."""
        if precio_min < 0:
            precio_min = 0
        resultados = []
        for mueble in self._inventario:
            try:
                precio = mueble.calcular_precio()
                if precio_min <= precio <= precio_max:
                    resultados.append(mueble)
            except Exception:
                continue
        return resultados

    def filtrar_por_material(self, material: str) -> List[Mueble]:
        """Filtra muebles por material."""
        if not material or not material.strip():
            return []
        material_lower = material.lower().strip()
        return [m for m in self._inventario if m.material.lower() == material_lower]

    def filtrar_por_color(self, color: str) -> List[Mueble]:
        """Filtra muebles por color."""
        if not color or not color.strip():
            return []
        color_lower = color.lower().strip()
        return [m for m in self._inventario if m.color.lower() == color_lower]

    def filtrar_por_tipo(self, tipo: str) -> List[Mueble]:
        """Filtra muebles por tipo (nombre de la clase)."""
        if not tipo or not tipo.strip():
            return []
        tipo_lower = tipo.lower().strip()
        return [m for m in self._inventario if type(m).__name__.lower() == tipo_lower]

    def obtener_muebles_por_tipo(self, tipo_clase: type) -> List[Mueble]:
        """Obtiene todos los muebles de un tipo específico."""
        return [m for m in self._inventario if isinstance(m, tipo_clase)]

    def calcular_inventario_total(self) -> float:
        """Calcula el valor total del inventario incluyendo comedores."""
        total = 0.0
        for mueble in self._inventario:
            try:
                total += mueble.calcular_precio()
            except Exception:
                continue
        total += sum(c.calcular_precio_total() for c in self._comedores)
        return round(total, 2)

    def calcular_valor_inventario(self) -> float:
        """Alias de calcular_inventario_total."""
        return self.calcular_inventario_total()

    def obtener_mueble_mas_caro(self) -> Optional[Mueble]:
        """Obtiene el mueble más caro del inventario."""
        if not self._inventario:
            return None
        try:
            return max(self._inventario, key=lambda m: m.calcular_precio())
        except Exception:
            return None

    def obtener_mueble_mas_barato(self) -> Optional[Mueble]:
        """Obtiene el mueble más barato del inventario."""
        if not self._inventario:
            return None
        try:
            return min(self._inventario, key=lambda m: m.calcular_precio())
        except Exception:
            return None

    def obtener_precio_promedio(self) -> float:
        """Calcula el precio promedio de los muebles en inventario."""
        if not self._inventario:
            return 0.0
        precios = []
        for mueble in self._inventario:
            try:
                precios.append(mueble.calcular_precio())
            except Exception:
                continue
        return round(sum(precios) / len(precios), 2) if precios else 0.0

    def aplicar_descuento(self, categoria: str, porcentaje: float) -> str:
        """
        Aplica un descuento a una categoría de muebles.

        Args:
            categoria: Nombre de la categoría (ej: "sillas", "mesas")
            porcentaje: Porcentaje de descuento (0-100)
        """
        if not 0 <= porcentaje <= 100:
            return "Error: El porcentaje debe estar entre 0 y 100"
        categoria_lower = categoria.lower().strip()
        self._descuentos_activos[categoria_lower] = porcentaje / 100
        return f"Descuento del {porcentaje}% aplicado a la categoría '{categoria}'"

    def realizar_venta(self, mueble_o_indice, cliente: str = "Cliente Anónimo") -> dict:
        """
        Procesa la venta de un mueble.

        Args:
            mueble_o_indice: Mueble o índice del mueble a vender
            cliente: Nombre del cliente
        """
        if isinstance(mueble_o_indice, int):
            if mueble_o_indice < 0 or mueble_o_indice >= len(self._inventario):
                return {"error": "Índice de mueble inválido"}
            mueble = self._inventario[mueble_o_indice]
        else:
            mueble = mueble_o_indice
            if mueble not in self._inventario:
                return {"error": "El mueble no está disponible en inventario"}
        try:
            precio_original = mueble.calcular_precio()
            descuento_aplicado = 0.0
            tipo_mueble = type(mueble).__name__.lower()
            if tipo_mueble in self._descuentos_activos:
                descuento_aplicado = self._descuentos_activos[tipo_mueble]
            precio_final = precio_original * (1 - descuento_aplicado)
            venta = {
                "mueble": mueble.nombre,
                "cliente": cliente,
                "tipo": type(mueble).__name__,
                "precio_original": precio_original,
                "descuento": descuento_aplicado * 100,
                "precio_final": round(precio_final, 2),
            }
            self._ventas_realizadas.append(venta)
            self._inventario.remove(mueble)
            return venta
        except Exception as e:
            return {"error": f"Error al procesar la venta: {str(e)}"}

    def obtener_total_ventas(self) -> float:
        """Calcula el total de ingresos por ventas."""
        total = sum(v.get("precio_final", 0) for v in self._ventas_realizadas)
        return round(total, 2)

    def _contar_tipos_muebles(self) -> Dict[str, int]:
        """Cuenta cuántos muebles hay de cada tipo."""
        conteo: Dict[str, int] = {}
        for mueble in self._inventario:
            tipo = type(mueble).__name__
            conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo

    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas generales de la tienda."""
        return {
            "total_muebles": len(self._inventario),
            "total_comedores": len(self._comedores),
            "valor_inventario": self.calcular_inventario_total(),
            "ventas_realizadas": len(self._ventas_realizadas),
            "tipos_muebles": self._contar_tipos_muebles(),
            "descuentos_activos": len(self._descuentos_activos),
        }

    def obtener_resumen_tienda(self) -> dict:
        """Obtiene un resumen completo de la tienda."""
        mas_caro = self.obtener_mueble_mas_caro()
        mas_barato = self.obtener_mueble_mas_barato()
        return {
            "nombre": self._nombre,
            "total_muebles": self.total_muebles,
            "total_comedores": self.total_comedores,
            "valor_inventario": self.calcular_inventario_total(),
            "precio_promedio": self.obtener_precio_promedio(),
            "mueble_mas_caro": mas_caro.nombre if mas_caro else "N/A",
            "mueble_mas_barato": mas_barato.nombre if mas_barato else "N/A",
            "total_ventas": self.total_ventas,
            "ingresos_totales": self.obtener_total_ventas(),
        }

    def generar_reporte_inventario(self) -> str:
        """Genera un reporte completo del inventario."""
        reporte = f"=== REPORTE DE INVENTARIO - {self._nombre} ===\n\n"
        estadisticas = self.obtener_estadisticas()
        reporte += f"Total de muebles: {estadisticas['total_muebles']}\n"
        reporte += f"Total de comedores: {estadisticas['total_comedores']}\n"
        reporte += f"Valor total del inventario: ${estadisticas['valor_inventario']:.2f}\n\n"
        reporte += "DISTRIBUCIÓN POR TIPOS:\n"
        for tipo, cantidad in estadisticas["tipos_muebles"].items():
            reporte += f"- {tipo}: {cantidad} unidades\n"
        if self._descuentos_activos:
            reporte += "\nDESCUENTOS ACTIVOS:\n"
            for categoria, descuento in self._descuentos_activos.items():
                reporte += f"- {categoria}: {descuento * 100:.1f}%\n"
        return reporte

    def mostrar_catalogo(self) -> str:
        """Genera un catálogo de todos los muebles disponibles."""
        if not self._inventario:
            return "El inventario está vacío"
        catalogo = f"\n📋 CATÁLOGO DE {self._nombre.upper()}\n"
        catalogo += "=" * 70 + "\n\n"
        for i, mueble in enumerate(self._inventario, 1):
            try:
                precio = mueble.calcular_precio()
                tipo = type(mueble).__name__
                catalogo += f"{i}. {mueble.nombre}\n"
                catalogo += f"   Tipo: {tipo} | Material: {mueble.material} | Color: {mueble.color}\n"
                catalogo += f"   Precio: ${precio}\n\n"
            except Exception as e:
                catalogo += f"{i}. {mueble.nombre} - Error: {str(e)}\n\n"
        catalogo += "=" * 70
        return catalogo

    def __str__(self) -> str:
        """Representación en cadena de la tienda."""
        return f"Tienda '{self._nombre}': {self.total_muebles} muebles, {self.total_comedores} comedores"
