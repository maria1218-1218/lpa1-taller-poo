"""
Pruebas unitarias para las clases de composición.
"""

import pytest
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.composicion.comedor import Comedor


class TestComedor:
    """
    Pruebas para la clase Comedor.
    Valida los conceptos de composición y agregación.
    """
    
    def setup_method(self):
        """Configuración que se ejecuta antes de cada test."""
        self.mesa = Mesa(
            nombre="Mesa Familiar",
            material="Madera",
            color="Roble",
            precio_base=500.0,
            largo=200.0,
            ancho=100.0,
            alto=75.0,
            material_superficie="madera"
        )
        
        self.sillas = []
        for i in range(4):
            silla = Silla(
                nombre=f"Silla {i+1}",
                material="Madera",
                color="Roble",
                precio_base=150.0,
                tiene_respaldo=True,
                material_tapizado="tela"
            )
            self.sillas.append(silla)
        
        self.comedor = Comedor(
            nombre="Comedor Completo",
            mesa=self.mesa,
            sillas=self.sillas
        )
    
    def test_creacion_comedor(self):
        """Prueba la creación correcta de un comedor."""
        assert self.comedor.nombre == "Comedor Completo"
        assert self.comedor.mesa == self.mesa
        assert self.comedor.numero_sillas == 4
    
    def test_agregar_silla(self):
        """Prueba agregar una silla al comedor."""
        silla_nueva = Silla(
            nombre="Silla Extra",
            material="Madera",
            color="Blanco",
            precio_base=150.0,
            tiene_respaldo=True
        )
        
        inicial = self.comedor.numero_sillas
        self.comedor.agregar_silla(silla_nueva)
        
        assert self.comedor.numero_sillas == inicial + 1
    
    def test_quitar_silla(self):
        """Prueba quitar una silla del comedor."""
        inicial = self.comedor.numero_sillas
        silla_removida = self.comedor.quitar_silla(0)
        
        assert self.comedor.numero_sillas == inicial - 1
        assert silla_removida.nombre == "Silla 1"
    
    def test_calcular_precio_total(self):
        """Prueba el cálculo del precio total del comedor."""
        precio_total = self.comedor.calcular_precio_total()
        
        # El precio total debe ser mesa + todas las sillas
        # Con descuento del 5% por tener 4 o más sillas
        assert precio_total > 0
        assert isinstance(precio_total, float)
    
    def test_descuento_set_completo(self):
        """Prueba que se aplica descuento con 4 o más sillas."""
        # Calcular precio sin descuento
        precio_sin_descuento = self.mesa.calcular_precio()
        for silla in self.sillas[:3]:  # Solo 3 sillas
            precio_sin_descuento += silla.calcular_precio()
        
        # Calcular precio con comedor de 4 sillas
        precio_con_comedor = self.comedor.calcular_precio_total()
        
        # El comedor debe aplicar descuento
        # precio_base * 0.95 < precio_sin_descuento
        assert precio_con_comedor < (self.mesa.calcular_precio() + sum(silla.calcular_precio() for silla in self.sillas))
    
    def test_limpiar_sillas(self):
        """Prueba limpiar todas las sillas del comedor."""
        self.comedor.limpiar_sillas()
        assert self.comedor.numero_sillas == 0
    
    def test_obtener_info_comedor(self):
        """Prueba que obtener_info_comedor retorna una cadena."""
        info = self.comedor.obtener_info_comedor()
        assert isinstance(info, str)
        assert len(info) > 0
        assert "Comedor Completo" in info
    
    def test_obtener_resumen(self):
        """Prueba que obtener_resumen retorna un diccionario correcto."""
        resumen = self.comedor.obtener_resumen()
        
        assert isinstance(resumen, dict)
        assert "nombre" in resumen
        assert "total_muebles" in resumen
        assert "precio_total" in resumen
        assert resumen["nombre"] == "Comedor Completo"
        assert resumen["numero_sillas"] == 4
    
    def test_str_comedor(self):
        """Prueba la representación en cadena del comedor."""
        str_comedor = str(self.comedor)
        assert isinstance(str_comedor, str)
        assert "Comedor Completo" in str_comedor
        assert "4" in str_comedor  # Debe mencionar las 4 sillas
    
    def test_len_comedor(self):
        """Prueba la longitud del comedor (mesa + sillas)."""
        # 1 mesa + 4 sillas = 5 muebles
        assert len(self.comedor) == 5

    def test_agregar_objeto_invalido(self):
        """No se pueden agregar objetos que no sean Silla."""
        with pytest.raises(TypeError):
            self.comedor.agregar_silla("no soy una silla")

    def test_quitar_silla_indice_invalido(self):
        """Índice fuera de rango lanza IndexError."""
        with pytest.raises(IndexError):
            self.comedor.quitar_silla(99)

    def test_precio_total_con_descuento(self):
        """4 sillas aplica descuento del 5%."""
        precio_total = self.comedor.calcular_precio_total()
        precio_sin_descuento = self.mesa.calcular_precio() + sum(
            s.calcular_precio() for s in self.sillas
        )
        assert precio_total == pytest.approx(precio_sin_descuento * 0.95, rel=1e-2)

    def test_setter_mesa_invalido(self):
        with pytest.raises(TypeError):
            self.comedor.mesa = "no soy una mesa"

    def test_setter_nombre_vacio(self):
        with pytest.raises(ValueError):
            self.comedor.nombre = ""

    def test_sillas_retorna_copia(self):
        """El getter de sillas retorna una copia para proteger encapsulación."""
        copia = self.comedor.sillas
        copia.append(Silla("Extra", "Metal", "Negro", 100.0))
        assert self.comedor.numero_sillas == 4  # lista interna no cambia
