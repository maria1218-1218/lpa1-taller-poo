"""
Pruebas unitarias para las clases de muebles.
Valida los conceptos OOP: abstracción, herencia, polimorfismo, encapsulación.
"""

import pytest
from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.categorias.superficies import Superficie
from models.categorias.almacenamiento import Almacenamiento
from models.concretos.silla import Silla
from models.concretos.sillon import Sillon
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.concretos.sofacama import SofaCama
from models.concretos.mesa import Mesa
from models.concretos.escritorio import Escritorio
from models.concretos.armario import Armario
from models.concretos.cajonera import Cajonera


class TestMuebleBase:
    """Pruebas para la clase base abstracta Mueble."""

    def test_no_puede_instanciar_mueble_directamente(self):
        with pytest.raises(TypeError):
            Mueble("Test", "Madera", "Café", 100.0)

    def test_no_puede_instanciar_asiento_directamente(self):
        with pytest.raises(TypeError):
            Asiento("Test", "Madera", "Café", 100.0, 1, True)

    def test_no_puede_instanciar_superficie_directamente(self):
        with pytest.raises(TypeError):
            Superficie("Test", "Madera", "Café", 100.0, 100, 80, 75, "madera")


class TestSilla:
    """Pruebas para la clase Silla."""

    def setup_method(self):
        self.silla_basica = Silla(
            nombre="Silla Básica",
            material="Madera",
            color="Café",
            precio_base=150.0,
            tiene_respaldo=True,
        )
        self.silla_oficina = Silla(
            nombre="Silla Oficina",
            material="Metal",
            color="Negro",
            precio_base=300.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        )

    def test_creacion_silla_basica(self):
        assert self.silla_basica.nombre == "Silla Básica"
        assert self.silla_basica.material == "Madera"
        assert self.silla_basica.color == "Café"
        assert self.silla_basica.precio_base == 150.0
        assert self.silla_basica.tiene_respaldo is True
        assert self.silla_basica.capacidad_personas == 1

    def test_calculo_precio_silla_basica(self):
        """precio_base=150, factor comodidad con respaldo=1.1 → 150*1.1=165.0"""
        precio = self.silla_basica.calcular_precio()
        assert precio == 165.0

    def test_calculo_precio_silla_oficina(self):
        precio = self.silla_oficina.calcular_precio()
        assert precio > self.silla_oficina.precio_base
        assert isinstance(precio, float)

    def test_es_silla_oficina_verdadero(self):
        assert self.silla_oficina.es_silla_oficina() is True

    def test_es_silla_oficina_falso(self):
        assert self.silla_basica.es_silla_oficina() is False

    def test_regular_altura_silla_sin_mecanismo(self):
        resultado = self.silla_basica.regular_altura(50)
        assert "regulable" in resultado.lower() or "no tiene" in resultado.lower()

    def test_regular_altura_silla_con_mecanismo(self):
        resultado = self.silla_oficina.regular_altura(55)
        assert "55" in resultado

    def test_regular_altura_invalida(self):
        resultado = self.silla_oficina.regular_altura(100)
        assert "inválida" in resultado.lower() or "invalida" in resultado.lower()

    def test_validaciones_setter_nombre_vacio(self):
        with pytest.raises(ValueError):
            self.silla_basica.nombre = ""

    def test_validaciones_setter_precio_negativo(self):
        with pytest.raises(ValueError):
            self.silla_basica.precio_base = -100

    def test_validaciones_setter_capacidad_cero(self):
        with pytest.raises(ValueError):
            self.silla_basica.capacidad_personas = 0

    def test_obtener_descripcion(self):
        descripcion = self.silla_basica.obtener_descripcion()
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion
        assert isinstance(descripcion, str)

    def test_polimorfismo_herencia(self):
        assert isinstance(self.silla_basica, Asiento)
        assert isinstance(self.silla_basica, Mueble)
        precio = self.silla_basica.calcular_precio()
        assert isinstance(precio, (int, float)) and precio > 0
        descripcion = self.silla_basica.obtener_descripcion()
        assert isinstance(descripcion, str) and len(descripcion) > 0

    def test_str(self):
        texto = str(self.silla_basica)
        assert "Madera" in texto and "Café" in texto


class TestSillon:
    """Pruebas para la clase Sillon."""

    def setup_method(self):
        self.sillon = Sillon("Sillón Test", "Cuero", "Marrón", 500.0,
                             tiene_brazos=True, material_tapizado="cuero")

    def test_creacion_sillon(self):
        assert self.sillon.nombre == "Sillón Test"
        assert self.sillon.tiene_brazos is True
        assert self.sillon.capacidad_personas == 1

    def test_precio_mayor_a_base(self):
        assert self.sillon.calcular_precio() > self.sillon.precio_base

    def test_descripcion_contiene_nombre(self):
        assert "Sillón Test" in self.sillon.obtener_descripcion()


class TestSofa:
    """Pruebas para la clase Sofa."""

    def setup_method(self):
        self.sofa = Sofa("Sofá Test", "Tela", "Gris", 800.0,
                         capacidad_personas=3, material_tapizado="tela", es_modular=True)

    def test_creacion_sofa(self):
        assert self.sofa.capacidad_personas == 3
        assert self.sofa.es_modular is True

    def test_precio_modular_mayor(self):
        sofa_normal = Sofa("N", "Tela", "Gris", 800.0, capacidad_personas=3)
        assert self.sofa.calcular_precio() > sofa_normal.calcular_precio()


class TestMesa:
    """Pruebas para la clase Mesa."""

    def setup_method(self):
        self.mesa = Mesa("Mesa Test", "Madera", "Roble", 500.0,
                         largo=180.0, ancho=90.0, alto=75.0, material_superficie="madera")

    def test_creacion_mesa(self):
        assert self.mesa.nombre == "Mesa Test"
        assert self.mesa.largo == 180.0

    def test_area_superficie(self):
        assert self.mesa.calcular_area_superficie() == 180.0 * 90.0

    def test_precio_mayor_a_base(self):
        assert self.mesa.calcular_precio() > self.mesa.precio_base

    def test_herencia_superficie(self):
        assert isinstance(self.mesa, Superficie)
        assert isinstance(self.mesa, Mueble)


class TestSofaCama:
    """Pruebas para la clase SofaCama (herencia múltiple)."""

    def setup_method(self):
        self.sofacama = SofaCama(
            nombre="SofaCama Deluxe",
            material="Tela",
            color="Gris",
            precio_base=1200.0,
            capacidad_personas=3,
            material_tapizado="tela",
            tamaño_cama="matrimonial",
            incluye_colchon=True,
            mecanismo_conversion="plegable",
        )

    def test_creacion_sofacama(self):
        assert self.sofacama.nombre == "SofaCama Deluxe"
        assert self.sofacama.capacidad_personas == 3
        assert self.sofacama.tamaño_cama == "matrimonial"
        assert self.sofacama.incluye_colchon is True
        assert self.sofacama.mecanismo_conversion == "plegable"
        assert self.sofacama.modo_actual == "sofa"

    def test_conversion_modos(self):
        assert self.sofacama.modo_actual == "sofa"
        resultado = self.sofacama.convertir_a_cama()
        assert "convertido a cama" in resultado.lower()
        assert self.sofacama.modo_actual == "cama"
        resultado2 = self.sofacama.convertir_a_cama()
        assert "ya está en modo cama" in resultado2.lower()
        resultado3 = self.sofacama.convertir_a_sofa()
        assert "convertida a sofá" in resultado3.lower()
        assert self.sofacama.modo_actual == "sofa"

    def test_calculo_precio_dual(self):
        precio = self.sofacama.calcular_precio()
        assert precio > self.sofacama.precio_base
        assert isinstance(precio, float)

    def test_capacidad_total(self):
        capacidades = self.sofacama.obtener_capacidad_total()
        assert "como_sofa" in capacidades
        assert "como_cama" in capacidades
        assert capacidades["como_sofa"] == 3

    def test_herencia_multiple_mro(self):
        from models.concretos.sofa import Sofa
        from models.concretos.cama import Cama
        assert isinstance(self.sofacama, Sofa)
        assert isinstance(self.sofacama, Cama)
        assert isinstance(self.sofacama, Asiento)
        assert isinstance(self.sofacama, Mueble)

    def test_tamaño_invalido(self):
        with pytest.raises(ValueError):
            self.sofacama.tamaño_cama = "gigante"

    def test_str(self):
        texto = str(self.sofacama)
        assert "sofa" in texto.lower() or "sofá" in texto.lower()


class TestArmario:
    """Pruebas para la clase Armario."""

    def setup_method(self):
        self.armario = Armario("Armario Test", "Madera", "Blanco", 600.0,
                               capacidad_volumen=3.5, numero_compartimientos=4,
                               tiene_espejo=True, numero_puertas=2)

    def test_herencia_almacenamiento(self):
        assert isinstance(self.armario, Almacenamiento)
        assert isinstance(self.armario, Mueble)

    def test_precio_mayor_a_base(self):
        assert self.armario.calcular_precio() > self.armario.precio_base

    def test_descripcion_valida(self):
        assert "Armario Test" in self.armario.obtener_descripcion()


class TestConceptosOOPGenerales:
    """Pruebas que validan conceptos generales de OOP en todo el sistema."""

    def test_polimorfismo_calcular_precio(self):
        """Distintos muebles calculan precios de forma polimórfica."""
        muebles: list = [
            Silla("S", "Madera", "Café", 100.0),
            Mesa("M", "Madera", "Roble", 100.0, 100, 80, 75, "madera"),
            Armario("A", "Madera", "Blanco", 100.0, 2.0, 3),
        ]
        precios = [m.calcular_precio() for m in muebles]
        assert all(p > 0 for p in precios)
        assert len(set(precios)) > 1

    def test_encapsulacion_atributos_privados(self):
        """Los atributos se almacenan como privados."""
        silla = Silla("Test", "Madera", "Café", 100.0)
        assert hasattr(silla, "_nombre")
        assert hasattr(silla, "_precio_base")

    def test_herencia_jerarquia(self):
        """La jerarquía de herencia funciona correctamente."""
        silla = Silla("Test", "Madera", "Café", 100.0)
        assert isinstance(silla, Silla)
        assert isinstance(silla, Asiento)
        assert isinstance(silla, Mueble)

    def test_todos_implementan_metodos_abstractos(self):
        """Todas las clases concretas implementan calcular_precio y obtener_descripcion."""
        concretos: list = [
            Silla("S", "Madera", "Café", 100.0),
            Sillon("Sl", "Cuero", "Marrón", 200.0),
            Sofa("So", "Tela", "Gris", 300.0),
            Cama("C", "Madera", "Blanco", 400.0),
            Mesa("M", "Madera", "Roble", 100.0, 100, 80, 75, "madera"),
            Escritorio("E", "Madera", "Café", 200.0, 120, 60, 75, "madera"),
            Armario("A", "Madera", "Blanco", 300.0, 2.0, 3),
            Cajonera("Ca", "Metal", "Gris", 150.0, 1.0, 3),
        ]
        for mueble in concretos:
            precio = mueble.calcular_precio()
            assert isinstance(precio, (int, float)) and precio > 0
            desc = mueble.obtener_descripcion()
            assert isinstance(desc, str) and len(desc) > 0


@pytest.fixture
def muebles_de_prueba():
    """Fixture con muebles básicos para múltiples tests."""
    return {
        "silla": Silla("Silla Test", "Madera", "Café", 100.0, True),
        "mesa": Mesa("Mesa Test", "Madera", "Roble", 300.0, 120, 80, 75, "madera"),
        "sofacama": SofaCama("SofaCama Test", "Tela", "Gris", 800.0),
    }


class TestIntegracion:
    """Pruebas de integración que validan el funcionamiento conjunto."""

    def test_creacion_tienda_completa(self):
        from services.tienda import TiendaMuebles
        tienda = TiendaMuebles("Tienda Test")
        silla = Silla("S1", "Madera", "Café", 150.0)
        mesa = Mesa("M1", "Madera", "Roble", 500.0, 180, 90, 75, "madera")
        tienda.agregar_mueble(silla)
        tienda.agregar_mueble(mesa)
        assert tienda.total_muebles == 2
        resultados = tienda.buscar_muebles_por_nombre("S1")
        assert len(resultados) == 1
        assert resultados[0].nombre == "S1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
