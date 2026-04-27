"""
Pruebas unitarias para la Tienda.
"""

import pytest
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.composicion.comedor import Comedor


class TestTiendaMuebles:
    """
    Pruebas para la clase TiendaMuebles.
    Valida la gestión del inventario y operaciones de tienda.
    """
    
    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        self.tienda = TiendaMuebles("Tienda Test")
        
        # Crear algunos muebles de prueba
        self.silla1 = Silla(
            nombre="Silla Test 1",
            material="Madera",
            color="Café",
            precio_base=150.0,
            tiene_respaldo=True
        )
        
        self.silla2 = Silla(
            nombre="Silla Test 2",
            material="Metal",
            color="Negro",
            precio_base=200.0,
            tiene_respaldo=True,
            material_tapizado="cuero"
        )
        
        self.mesa = Mesa(
            nombre="Mesa Test",
            material="Madera",
            color="Blanco",
            precio_base=500.0,
            largo=150.0,
            ancho=80.0,
            alto=75.0,
            material_superficie="madera"
        )
    
    def test_creacion_tienda(self):
        """Prueba la creación de una tienda."""
        assert self.tienda.nombre == "Tienda Test"
        assert self.tienda.total_muebles == 0
    
    def test_agregar_mueble(self):
        """Prueba agregar muebles a la tienda."""
        resultado = self.tienda.agregar_mueble(self.silla1)
        
        assert "exitosamente" in resultado
        assert self.tienda.total_muebles == 1
    
    def test_agregar_multiples_muebles(self):
        """Prueba agregar múltiples muebles."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.silla2)
        self.tienda.agregar_mueble(self.mesa)
        
        assert self.tienda.total_muebles == 3
    
    def test_agregar_mueble_invalido(self):
        """Prueba que no se pueden agregar objetos inválidos."""
        resultado = self.tienda.agregar_mueble("no es un mueble")
        
        assert "Error" in resultado
    
    def test_buscar_muebles_por_nombre(self):
        """Prueba la búsqueda de muebles por nombre."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.mesa)
        
        resultados = self.tienda.buscar_muebles_por_nombre("Silla")
        
        assert len(resultados) == 1
        assert resultados[0].nombre == "Silla Test 1"
    
    def test_filtrar_por_precio(self):
        """Prueba filtrar muebles por precio."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.silla2)
        self.tienda.agregar_mueble(self.mesa)
        
        resultados = self.tienda.filtrar_por_precio(180.0, 600.0)
        
        # Debe incluir silla2 y mesa
        assert len(resultados) >= 1
    
    def test_filtrar_por_material(self):
        """Prueba filtrar muebles por material."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.silla2)
        self.tienda.agregar_mueble(self.mesa)
        
        resultados = self.tienda.filtrar_por_material("Madera")
        
        assert len(resultados) >= 2
    
    def test_filtrar_por_color(self):
        """Prueba filtrar muebles por color."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.mesa)
        
        resultados = self.tienda.filtrar_por_color("Café")
        
        assert len(resultados) == 1
        assert resultados[0].color == "Café"
    
    def test_calcular_inventario_total(self):
        """Prueba el cálculo del valor total del inventario."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.silla2)
        
        total = self.tienda.calcular_inventario_total()
        
        assert total > 0
        # Debe ser mayor que la suma de precios base
        assert total >= self.silla1.precio_base + self.silla2.precio_base
    
    def test_obtener_mueble_mas_caro(self):
        """Prueba obtener el mueble más caro."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.mesa)  # Más caro
        
        mas_caro = self.tienda.obtener_mueble_mas_caro()
        
        assert mas_caro.nombre == "Mesa Test"
    
    def test_obtener_mueble_mas_barato(self):
        """Prueba obtener el mueble más barato."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.mesa)
        
        mas_barato = self.tienda.obtener_mueble_mas_barato()
        
        assert mas_barato.nombre == "Silla Test 1"
    
    def test_obtener_precio_promedio(self):
        """Prueba el cálculo del precio promedio."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.silla2)
        
        promedio = self.tienda.obtener_precio_promedio()
        
        assert promedio > 0
        assert isinstance(promedio, float)
    
    def test_obtener_resumen_tienda(self):
        """Prueba obtener el resumen de la tienda."""
        self.tienda.agregar_mueble(self.silla1)
        self.tienda.agregar_mueble(self.mesa)
        
        resumen = self.tienda.obtener_resumen_tienda()
        
        assert isinstance(resumen, dict)
        assert "total_muebles" in resumen
        assert resumen["total_muebles"] == 2
        assert "valor_inventario" in resumen
    
    def test_agregar_comedor(self):
        """Prueba agregar un comedor a la tienda."""
        mesa_comedor = Mesa(
            nombre="Mesa Comedor",
            material="Madera",
            color="Roble",
            precio_base=600.0,
            largo=180.0,
            ancho=90.0,
            alto=75.0,
            material_superficie="madera"
        )
        
        sillas = [
            Silla(
                nombre=f"Silla Comedor {i}",
                material="Madera",
                color="Roble",
                precio_base=120.0,
                tiene_respaldo=True
            )
            for i in range(4)
        ]
        
        comedor = Comedor(
            nombre="Comedor Familiar",
            mesa=mesa_comedor,
            sillas=sillas
        )
        
        resultado = self.tienda.agregar_comedor(comedor)
        
        assert "exitosamente" in resultado
        assert self.tienda.total_comedores == 1

    def test_obtener_estadisticas(self):
        """Prueba que las estadísticas incluyen todos los campos."""
        self.tienda.agregar_mueble(self.silla1)
        stats = self.tienda.obtener_estadisticas()
        assert "total_muebles" in stats
        assert "total_comedores" in stats
        assert "valor_inventario" in stats
        assert "ventas_realizadas" in stats
        assert "tipos_muebles" in stats
        assert stats["total_muebles"] == 1

    def test_aplicar_descuento(self):
        """Prueba aplicar descuento a una categoría."""
        resultado = self.tienda.aplicar_descuento("silla", 10)
        assert "10%" in resultado or "Descuento" in resultado

    def test_aplicar_descuento_invalido(self):
        """Prueba que un porcentaje fuera de rango devuelve error."""
        resultado = self.tienda.aplicar_descuento("silla", 110)
        assert "Error" in resultado

    def test_realizar_venta(self):
        """Prueba realizar una venta de un mueble."""
        self.tienda.agregar_mueble(self.silla1)
        total_antes = self.tienda.total_muebles
        venta = self.tienda.realizar_venta(self.silla1)
        assert "precio_final" in venta
        assert self.tienda.total_muebles == total_antes - 1

    def test_realizar_venta_mueble_no_disponible(self):
        """Prueba que no se puede vender un mueble que no está en inventario."""
        silla_externa = Silla("Externa", "Madera", "Café", 100.0)
        resultado = self.tienda.realizar_venta(silla_externa)
        assert "error" in resultado

    def test_eliminar_mueble(self):
        """Prueba eliminar un mueble por índice."""
        self.tienda.agregar_mueble(self.silla1)
        resultado = self.tienda.eliminar_mueble(0)
        assert "eliminado" in resultado
        assert self.tienda.total_muebles == 0

    def test_generar_reporte_inventario(self):
        """Prueba que el reporte de inventario se genera correctamente."""
        self.tienda.agregar_mueble(self.silla1)
        reporte = self.tienda.generar_reporte_inventario()
        assert isinstance(reporte, str)
        assert len(reporte) > 0
        assert "Tienda Test" in reporte

    def test_inventario_vacio_sin_mas_caro(self):
        """Prueba que con inventario vacío obtener_mueble_mas_caro retorna None."""
        assert self.tienda.obtener_mueble_mas_caro() is None
        assert self.tienda.obtener_mueble_mas_barato() is None

    def test_str_tienda(self):
        """Prueba la representación en cadena de la tienda."""
        texto = str(self.tienda)
        assert "Tienda Test" in texto


class TestCatalogo:
    """Pruebas para la clase Catalogo."""

    def setup_method(self):
        from services.catalogo import Catalogo
        self.catalogo = Catalogo("Catálogo Test")
        self.silla = Silla("Silla Cat", "Madera", "Café", 100.0)
        self.mesa = Mesa("Mesa Cat", "Madera", "Roble", 300.0,
                         120.0, 80.0, 75.0, "madera")

    def test_creacion_catalogo(self):
        from services.catalogo import Catalogo
        assert self.catalogo.nombre == "Catálogo Test"
        assert self.catalogo.total_items() == 0

    def test_agregar_item(self):
        self.catalogo.agregar_item(self.silla, "Asientos")
        assert self.catalogo.total_items() == 1

    def test_agregar_item_invalido(self):
        with pytest.raises(TypeError):
            self.catalogo.agregar_item("no es mueble", "Test")

    def test_obtener_por_categoria(self):
        self.catalogo.agregar_item(self.silla, "Asientos")
        self.catalogo.agregar_item(self.mesa, "Superficies")
        asientos = self.catalogo.obtener_por_categoria("Asientos")
        assert len(asientos) == 1
        assert asientos[0] == self.silla

    def test_buscar_por_nombre(self):
        self.catalogo.agregar_item(self.silla, "Asientos")
        self.catalogo.agregar_item(self.mesa, "Superficies")
        resultados = self.catalogo.buscar_por_nombre("Silla")
        assert len(resultados) == 1

    def test_valor_total(self):
        self.catalogo.agregar_item(self.silla, "Asientos")
        self.catalogo.agregar_item(self.mesa, "Superficies")
        total = self.catalogo.calcular_valor_total()
        assert total > 0

    def test_len(self):
        self.catalogo.agregar_item(self.silla, "Asientos")
        assert len(self.catalogo) == 1
