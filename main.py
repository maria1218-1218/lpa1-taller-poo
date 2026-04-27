#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Tienda de Muebles.
"""

from services.tienda import TiendaMuebles
from ui.menu import MenuTienda

from models.concretos.silla import Silla
from models.concretos.sillon import Sillon
from models.concretos.sofa import Sofa
from models.concretos.mesa import Mesa
from models.concretos.armario import Armario
from models.concretos.cama import Cama
from models.concretos.escritorio import Escritorio
from models.concretos.cajonera import Cajonera
from models.concretos.sofacama import SofaCama
from models.composicion.comedor import Comedor


def crear_catalogo_inicial(tienda: TiendaMuebles) -> None:
    """Crea un catálogo inicial de muebles para demostrar el funcionamiento."""
    print("🔨 Creando catálogo inicial de muebles...")

    sillas = [
        Silla("Silla Clásica", "Madera", "Café", 150.0,
              tiene_respaldo=True, material_tapizado="tela"),
        Silla("Silla de Oficina Ejecutiva", "Metal", "Negro", 350.0,
              tiene_respaldo=True, material_tapizado="cuero",
              altura_regulable=True, tiene_ruedas=True),
        Silla("Silla Moderna Minimalista", "Plástico", "Blanco", 80.0,
              tiene_respaldo=True),
    ]

    mesas = [
        Mesa("Mesa de Comedor Familiar", "Madera", "Roble", 500.0,
             largo=180.0, ancho=90.0, alto=75.0, material_superficie="madera"),
        Mesa("Mesa de Centro Redonda", "Vidrio", "Transparente", 300.0,
             largo=100.0, ancho=100.0, alto=45.0, material_superficie="vidrio"),
        Mesa("Mesa de Trabajo Industrial", "Metal", "Gris", 450.0,
             largo=150.0, ancho=75.0, alto=85.0, material_superficie="fórmica"),
    ]

    asientos_grandes = [
        Sillon("Sillón Reclinable de Lujo", "Cuero", "Marrón", 800.0,
               tiene_brazos=True, material_tapizado="cuero"),
        Sofa("Sofá Modular de 3 Plazas", "Tela", "Gris", 1200.0,
             capacidad_personas=3, material_tapizado="tela", es_modular=True),
        Sofa("Sofá Chesterfield Clásico", "Cuero", "Verde", 2000.0,
             capacidad_personas=2, material_tapizado="cuero", es_modular=False),
    ]

    almacenamiento = [
        Armario("Armario Ropero 2 Puertas", "Madera", "Blanco", 600.0,
                capacidad_volumen=3.5, numero_compartimientos=4,
                tiene_espejo=True, numero_puertas=2),
        Cajonera("Cajonera Vintage 5 Cajones", "Madera", "Café", 300.0,
                 capacidad_volumen=2.0, numero_compartimientos=5,
                 profundidad_cajones=50.0, deslizable=False),
        Cajonera("Cajonera Oficina con Ruedas", "Metal", "Gris", 180.0,
                 capacidad_volumen=1.5, numero_compartimientos=3,
                 profundidad_cajones=45.0, deslizable=True),
    ]

    dormitorio_oficina = [
        Cama("Cama King Size de Lujo", "Madera", "Nogal", 1000.0,
             tamaño="king", tiene_almacenamiento=True, es_electrica=False),
        Cama("Cama Double con Almacenamiento", "Madera", "Blanco", 400.0,
             tamaño="double", tiene_almacenamiento=True, es_electrica=False),
        Escritorio("Escritorio Ejecutivo", "Madera", "Caoba", 750.0,
                   largo=160.0, ancho=80.0, alto=75.0, material_superficie="madera",
                   numero_cajones=4, tiene_cajonera=True, altura_regulable=False),
        Escritorio("Escritorio Gaming Moderno", "Metal", "Negro", 500.0,
                   largo=140.0, ancho=70.0, alto=75.0, material_superficie="fórmica",
                   numero_cajones=2, tiene_cajonera=False, altura_regulable=True),
    ]

    sofacama = SofaCama(
        "SofaCama Convertible Premium", "Tela", "Beige", 1500.0,
        capacidad_personas=3, material_tapizado="tela",
        tamaño_cama="queen", incluye_colchon=True, mecanismo_conversion="plegable",
    )

    for mueble in sillas + mesas + asientos_grandes + almacenamiento + dormitorio_oficina + [sofacama]:
        print(f"  {tienda.agregar_mueble(mueble)}")

    print("✅ Catálogo inicial creado con éxito!")


def crear_comedores_ejemplo(tienda: TiendaMuebles) -> None:
    """Crea comedores de ejemplo para demostrar la composición."""
    print("\n🍽️ Creando comedores de ejemplo...")

    mesa_familiar = Mesa("Mesa Familiar Extensible", "Madera", "Roble", 800.0,
                         largo=200.0, ancho=100.0, alto=75.0, material_superficie="madera")
    sillas_familiares = [
        Silla(f"Silla Familiar {i}", "Madera", "Roble", 120.0,
              tiene_respaldo=True, material_tapizado="tela")
        for i in range(1, 7)
    ]
    comedor_familiar = Comedor("Comedor Familiar Completo",
                               mesa=mesa_familiar, sillas=sillas_familiares)

    mesa_moderna = Mesa("Mesa Moderna Cristal", "Vidrio", "Negro", 600.0,
                        largo=120.0, ancho=120.0, alto=75.0, material_superficie="vidrio")
    sillas_modernas = [
        Silla(f"Silla Moderna {i}", "Metal", "Negro", 150.0,
              tiene_respaldo=True, material_tapizado="cuero")
        for i in range(1, 5)
    ]
    comedor_moderno = Comedor("Comedor Moderno Premium",
                              mesa=mesa_moderna, sillas=sillas_modernas)

    for comedor in [comedor_familiar, comedor_moderno]:
        print(f"  {tienda.agregar_comedor(comedor)}")

    print("✅ Comedores de ejemplo creados!")


def aplicar_descuentos_ejemplo(tienda: TiendaMuebles) -> None:
    """Aplica descuentos de ejemplo para demostrar el sistema."""
    print("\n🏷️ Aplicando descuentos de ejemplo...")
    for categoria, porcentaje in [("silla", 10), ("mesa", 15), ("sofa", 20)]:
        print(f"  {tienda.aplicar_descuento(categoria, porcentaje)}")
    print("✅ Descuentos aplicados!")


def mostrar_estadisticas_iniciales(tienda: TiendaMuebles) -> None:
    """Muestra estadísticas iniciales de la tienda."""
    print("\n📊 Estadísticas iniciales de la tienda:")
    stats = tienda.obtener_estadisticas()
    print(f"  📦 Total de muebles: {stats['total_muebles']}")
    print(f"  🍽️  Total de comedores: {stats['total_comedores']}")
    print(f"  💰 Valor del inventario: ${stats['valor_inventario']:,.2f}")
    print(f"  🏷️  Descuentos activos: {stats['descuentos_activos']}")
    print("\n  📋 Distribución por tipos:")
    for tipo, cantidad in stats["tipos_muebles"].items():
        print(f"    • {tipo}: {cantidad} unidades")


def main():
    """Función principal que inicializa y ejecuta la aplicación."""
    try:
        print("🏠 Bienvenido a la Tienda de Muebles - Taller OOP 🏠")
        print("=" * 50)

        tienda = TiendaMuebles("Mueblería Moderna OOP")
        print(f"🏪 Inicializando {tienda.nombre}...")

        crear_catalogo_inicial(tienda)
        crear_comedores_ejemplo(tienda)
        aplicar_descuentos_ejemplo(tienda)
        mostrar_estadisticas_iniciales(tienda)

        print("\n🎯 Iniciando interfaz de usuario...")
        menu = MenuTienda(tienda)

        input("\nPresiona Enter para iniciar el menú interactivo...")
        menu.ejecutar()

    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "=" * 50)
        print("✨ Programa finalizado. ¡Gracias por usar la Tienda de Muebles! ✨")


if __name__ == "__main__":
    main()
