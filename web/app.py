"""
Flask web application for Tienda de Muebles.
Run with: python web/app.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.sillon import Sillon
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.concretos.sofacama import SofaCama
from models.concretos.mesa import Mesa
from models.concretos.escritorio import Escritorio
from models.concretos.armario import Armario
from models.concretos.cajonera import Cajonera
from models.composicion.comedor import Comedor

app = Flask(__name__)
tienda = TiendaMuebles("Mueblería Moderna OOP")

FABRICAS = {
    "Silla": lambda d: Silla(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        tiene_respaldo=bool(d.get("tiene_respaldo", True)),
        material_tapizado=d.get("material_tapizado") or None,
        altura_regulable=bool(d.get("altura_regulable", False)),
        tiene_ruedas=bool(d.get("tiene_ruedas", False)),
    ),
    "Sillon": lambda d: Sillon(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        tiene_brazos=bool(d.get("tiene_brazos", True)),
        material_tapizado=d.get("material_tapizado") or "tela",
    ),
    "Sofa": lambda d: Sofa(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        capacidad_personas=int(d.get("capacidad_personas", 3)),
        material_tapizado=d.get("material_tapizado") or "tela",
        es_modular=bool(d.get("es_modular", False)),
    ),
    "Cama": lambda d: Cama(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        tamaño=d.get("tamaño", "queen"),
        tiene_almacenamiento=bool(d.get("tiene_almacenamiento", False)),
        es_electrica=bool(d.get("es_electrica", False)),
    ),
    "SofaCama": lambda d: SofaCama(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        capacidad_personas=int(d.get("capacidad_personas", 3)),
        material_tapizado=d.get("material_tapizado") or "tela",
        tamaño_cama=d.get("tamaño_cama", "queen"),
        incluye_colchon=bool(d.get("incluye_colchon", True)),
        mecanismo_conversion=d.get("mecanismo_conversion", "plegable"),
    ),
    "Mesa": lambda d: Mesa(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        largo=float(d.get("largo", 120)),
        ancho=float(d.get("ancho", 80)),
        alto=float(d.get("alto", 75)),
        material_superficie=d.get("material_superficie", "madera"),
    ),
    "Escritorio": lambda d: Escritorio(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        largo=float(d.get("largo", 120)),
        ancho=float(d.get("ancho", 60)),
        alto=float(d.get("alto", 75)),
        material_superficie=d.get("material_superficie", "madera"),
        numero_cajones=int(d.get("numero_cajones", 0)),
        tiene_cajonera=bool(d.get("tiene_cajonera", False)),
        altura_regulable=bool(d.get("altura_regulable", False)),
    ),
    "Armario": lambda d: Armario(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        capacidad_volumen=float(d.get("capacidad_volumen", 2.0)),
        numero_compartimientos=int(d.get("numero_compartimientos", 3)),
        tiene_espejo=bool(d.get("tiene_espejo", False)),
        numero_puertas=int(d.get("numero_puertas", 2)),
    ),
    "Cajonera": lambda d: Cajonera(
        d["nombre"], d["material"], d["color"], float(d["precio_base"]),
        capacidad_volumen=float(d.get("capacidad_volumen", 1.5)),
        numero_compartimientos=int(d.get("numero_compartimientos", 3)),
        profundidad_cajones=float(d.get("profundidad_cajones", 45.0)),
        deslizable=bool(d.get("deslizable", False)),
    ),
}


def _cargar_datos_iniciales():
    muebles = [
        Silla("Silla Clásica", "Madera", "Café", 150.0,
              tiene_respaldo=True, material_tapizado="tela"),
        Silla("Silla de Oficina Ejecutiva", "Metal", "Negro", 350.0,
              tiene_respaldo=True, material_tapizado="cuero",
              altura_regulable=True, tiene_ruedas=True),
        Silla("Silla Moderna Minimalista", "Plástico", "Blanco", 80.0,
              tiene_respaldo=True),
        Sillon("Sillón Reclinable de Lujo", "Cuero", "Marrón", 800.0,
               tiene_brazos=True, material_tapizado="cuero"),
        Sofa("Sofá Modular 3 Plazas", "Tela", "Gris", 1200.0,
             capacidad_personas=3, material_tapizado="tela", es_modular=True),
        Sofa("Sofá Chesterfield Clásico", "Cuero", "Verde", 2000.0,
             capacidad_personas=2, material_tapizado="cuero"),
        Mesa("Mesa de Comedor Familiar", "Madera", "Roble", 500.0,
             largo=180.0, ancho=90.0, alto=75.0, material_superficie="madera"),
        Mesa("Mesa de Centro", "Vidrio", "Transparente", 300.0,
             largo=100.0, ancho=100.0, alto=45.0, material_superficie="vidrio"),
        Mesa("Mesa de Trabajo Industrial", "Metal", "Gris", 450.0,
             largo=150.0, ancho=75.0, alto=85.0, material_superficie="formica"),
        Armario("Armario Ropero 2 Puertas", "Madera", "Blanco", 600.0,
                capacidad_volumen=3.5, numero_compartimientos=4,
                tiene_espejo=True, numero_puertas=2),
        Cajonera("Cajonera Vintage 5 Cajones", "Madera", "Café", 300.0,
                 capacidad_volumen=2.0, numero_compartimientos=5,
                 profundidad_cajones=50.0, deslizable=False),
        Cajonera("Cajonera Oficina con Ruedas", "Metal", "Gris", 180.0,
                 capacidad_volumen=1.5, numero_compartimientos=3,
                 profundidad_cajones=45.0, deslizable=True),
        Cama("Cama King Size de Lujo", "Madera", "Nogal", 1000.0,
             tamaño="king", tiene_almacenamiento=True),
        Cama("Cama Double con Almacenamiento", "Madera", "Blanco", 400.0,
             tamaño="double", tiene_almacenamiento=True),
        Escritorio("Escritorio Ejecutivo", "Madera", "Caoba", 750.0,
                   largo=160.0, ancho=80.0, alto=75.0,
                   material_superficie="madera", numero_cajones=4, tiene_cajonera=True),
        Escritorio("Escritorio Gaming", "Metal", "Negro", 500.0,
                   largo=140.0, ancho=70.0, alto=75.0,
                   material_superficie="formica", numero_cajones=2,
                   altura_regulable=True),
        SofaCama("SofaCama Convertible Premium", "Tela", "Beige", 1500.0,
                 capacidad_personas=3, material_tapizado="tela",
                 tamaño_cama="queen", incluye_colchon=True,
                 mecanismo_conversion="plegable"),
    ]
    for m in muebles:
        tienda.agregar_mueble(m)

    mesa_c1 = Mesa("Mesa Familiar Extensible", "Madera", "Roble", 800.0,
                   largo=200.0, ancho=100.0, alto=75.0, material_superficie="madera")
    sillas_c1 = [
        Silla(f"Silla Familiar {i}", "Madera", "Roble", 120.0,
              tiene_respaldo=True, material_tapizado="tela")
        for i in range(1, 7)
    ]
    tienda.agregar_comedor(Comedor("Comedor Familiar Completo",
                                   mesa=mesa_c1, sillas=sillas_c1))

    mesa_c2 = Mesa("Mesa Moderna Cristal", "Vidrio", "Negro", 600.0,
                   largo=120.0, ancho=120.0, alto=75.0,
                   material_superficie="vidrio")
    sillas_c2 = [
        Silla(f"Silla Moderna {i}", "Metal", "Negro", 150.0,
              tiene_respaldo=True, material_tapizado="cuero")
        for i in range(1, 5)
    ]
    tienda.agregar_comedor(Comedor("Comedor Moderno Premium",
                                   mesa=mesa_c2, sillas=sillas_c2))

    tienda.aplicar_descuento("silla", 10)
    tienda.aplicar_descuento("mesa", 15)


_cargar_datos_iniciales()


def mueble_to_dict(mueble, idx):
    return {
        "id": idx,
        "nombre": mueble.nombre,
        "tipo": type(mueble).__name__,
        "material": mueble.material,
        "color": mueble.color,
        "precio_base": mueble.precio_base,
        "precio_final": round(mueble.calcular_precio(), 2),
        "descripcion": mueble.obtener_descripcion(),
    }


def comedor_to_dict(comedor, idx):
    r = comedor.obtener_resumen()
    return {
        "id": idx,
        "nombre": comedor.nombre,
        "numero_sillas": comedor.numero_sillas,
        "precio_total": round(comedor.calcular_precio_total(), 2),
        "precio_mesa": round(comedor.mesa.calcular_precio(), 2),
        "precio_sillas": round(r["precio_sillas_total"], 2),
        "tiene_descuento": r["tiene_descuento"],
        "descripcion": comedor.obtener_info_comedor(),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/inventario")
def get_inventario():
    return jsonify([mueble_to_dict(m, i)
                    for i, m in enumerate(tienda._inventario)])


@app.route("/api/inventario", methods=["POST"])
def add_mueble():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400
    tipo = data.get("tipo")
    if tipo not in FABRICAS:
        return jsonify({"error": f"Tipo desconocido: {tipo}"}), 400
    try:
        mueble = FABRICAS[tipo](data)
        resultado = tienda.agregar_mueble(mueble)
        if "Error" in resultado:
            return jsonify({"error": resultado}), 400
        return jsonify({
            "mensaje": resultado,
            "mueble": mueble_to_dict(mueble, tienda.total_muebles - 1),
        }), 201
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/inventario/<int:idx>", methods=["DELETE"])
def delete_mueble(idx):
    resultado = tienda.eliminar_mueble(idx)
    if "Error" in resultado:
        return jsonify({"error": resultado}), 404
    return jsonify({"mensaje": resultado})


@app.route("/api/buscar")
def buscar():
    q = request.args.get("q", "").strip()
    material = request.args.get("material", "").strip()
    color = request.args.get("color", "").strip()
    tipo = request.args.get("tipo", "").strip()
    min_precio = request.args.get("min_precio", type=float)
    max_precio = request.args.get("max_precio", type=float)

    resultado = list(tienda._inventario)
    if q:
        resultado = [m for m in resultado if q.lower() in m.nombre.lower()]
    if material:
        resultado = [m for m in resultado if m.material.lower() == material.lower()]
    if color:
        resultado = [m for m in resultado if m.color.lower() == color.lower()]
    if tipo:
        resultado = [m for m in resultado
                     if type(m).__name__.lower() == tipo.lower()]
    if min_precio is not None:
        resultado = [m for m in resultado if m.calcular_precio() >= min_precio]
    if max_precio is not None:
        resultado = [m for m in resultado if m.calcular_precio() <= max_precio]

    indices = {id(m): i for i, m in enumerate(tienda._inventario)}
    return jsonify([mueble_to_dict(m, indices[id(m)]) for m in resultado])


@app.route("/api/comedores")
def get_comedores():
    return jsonify([comedor_to_dict(c, i)
                    for i, c in enumerate(tienda._comedores)])


@app.route("/api/estadisticas")
def get_estadisticas():
    return jsonify({**tienda.obtener_estadisticas(),
                    **tienda.obtener_resumen_tienda()})


@app.route("/api/ventas")
def get_ventas():
    return jsonify({
        "ventas": tienda._ventas_realizadas,
        "total": tienda.obtener_total_ventas(),
    })


@app.route("/api/ventas", methods=["POST"])
def realizar_venta():
    data = request.get_json()
    idx = data.get("indice")
    cliente = data.get("cliente", "Cliente Anónimo")
    resultado = tienda.realizar_venta(idx, cliente)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado)


@app.route("/api/descuentos", methods=["POST"])
def aplicar_descuento():
    data = request.get_json()
    categoria = data.get("categoria", "")
    porcentaje = data.get("porcentaje", 0)
    resultado = tienda.aplicar_descuento(categoria, porcentaje)
    if "Error" in resultado:
        return jsonify({"error": resultado}), 400
    return jsonify({"mensaje": resultado})


if __name__ == "__main__":
    print("Iniciando Mueblería Web en http://localhost:5000")
    app.run(debug=True, port=5000)
