"""
Interfaz de usuario usando Rich para crear un menú interactivo y atractivo.
"""

import time
from typing import List

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text

from services.tienda import TiendaMuebles
from models.mueble import Mueble


class MenuTienda:
    """
    Clase que maneja la interfaz de usuario de la tienda usando Rich.

    Conceptos aplicados:
    - Separación de responsabilidades: UI separada de la lógica de negocio
    - Encapsulación: Agrupa toda la lógica de interfaz
    - Composición: Usa una instancia de TiendaMuebles para las operaciones
    """

    def __init__(self, tienda: TiendaMuebles):
        self.tienda = tienda
        self.console = Console()
        self.running = True

    def mostrar_banner(self):
        """Muestra el banner de bienvenida de la tienda."""
        banner_text = Text(f"🏠  {self.tienda.nombre}  🏠", style="bold magenta")
        panel = Panel(
            banner_text,
            title="Bienvenido",
            subtitle="Tu tienda de muebles favorita",
            border_style="blue",
        )
        self.console.print(panel)
        self.console.print()

    def mostrar_menu_principal(self) -> int:
        """
        Muestra el menú principal y obtiene la selección del usuario.

        Returns:
            int: Opción seleccionada (0 = salir)
        """
        menu_text = Text()
        menu_text.append("🔹 MENÚ PRINCIPAL 🔹\n\n", style="bold cyan")
        opciones = [
            "1. Ver catálogo completo",
            "2. Buscar muebles por nombre",
            "3. Filtrar por precio",
            "4. Filtrar por material",
            "5. Ver comedores disponibles",
            "6. Realizar venta",
            "7. Ver estadísticas",
            "8. Generar reporte de inventario",
            "9. Aplicar descuentos",
            "0. Salir",
        ]
        for opcion in opciones:
            menu_text.append(f"{opcion}\n", style="green")
        panel = Panel(
            menu_text,
            title="Opciones Disponibles",
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(panel)
        try:
            return IntPrompt.ask(
                "Selecciona una opción",
                choices=[str(i) for i in range(0, 10)],
            )
        except Exception:
            return self.mostrar_menu_principal()

    def mostrar_catalogo_completo(self):
        """Muestra todos los muebles disponibles en una tabla."""
        muebles = self.tienda._inventario
        if not muebles:
            self.console.print("[yellow]📭 No hay muebles en el inventario.[/yellow]")
            return
        table = Table(title="📋 Catálogo de Muebles")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nombre", style="magenta")
        table.add_column("Tipo", style="green")
        table.add_column("Material", style="yellow")
        table.add_column("Color", style="blue")
        table.add_column("Precio", style="red", justify="right")
        for i, mueble in enumerate(muebles, 1):
            try:
                precio = f"${mueble.calcular_precio():.2f}"
                tipo = type(mueble).__name__
                table.add_row(
                    str(i), mueble.nombre, tipo,
                    mueble.material, mueble.color, precio,
                )
            except Exception:
                table.add_row(str(i), mueble.nombre, "Error", "-", "-", "Error")
        self.console.print(table)

    def buscar_muebles_interactivo(self):
        """Interfaz interactiva para buscar muebles."""
        termino = Prompt.ask("[green]🔍 Ingresa el nombre o parte del nombre a buscar[/green]")
        if not termino.strip():
            self.console.print("[red]❌ Término de búsqueda vacío.[/red]")
            return
        with self.console.status("[bold green]Buscando muebles..."):
            time.sleep(0.5)
            resultados = self.tienda.buscar_muebles_por_nombre(termino)
        if not resultados:
            self.console.print(f"[yellow]❌ No se encontraron muebles con '{termino}'.[/yellow]")
            return
        self.console.print(f"\n[green]✓ Se encontraron {len(resultados)} resultado(s):[/green]")
        self._mostrar_lista_muebles(resultados)

    def filtrar_por_precio_interactivo(self):
        """Interfaz interactiva para filtrar por precio."""
        self.console.print("[cyan]💰 Filtrar muebles por rango de precio[/cyan]")
        precio_min = IntPrompt.ask("Precio mínimo", default=0, show_default=True)
        precio_max = IntPrompt.ask("Precio máximo (0 = sin límite)", default=0, show_default=True)
        precio_max_real = float('inf') if precio_max == 0 else float(precio_max)
        if precio_min > precio_max_real:
            self.console.print("[red]❌ El precio mínimo no puede ser mayor al máximo.[/red]")
            return
        with self.console.status("[bold green]Filtrando muebles..."):
            time.sleep(0.3)
            resultados = self.tienda.filtrar_por_precio(precio_min, precio_max_real)
        if not resultados:
            self.console.print("[yellow]❌ No hay muebles en ese rango de precios.[/yellow]")
            return
        self.console.print(f"\n[green]✓ Se encontraron {len(resultados)} mueble(s):[/green]")
        self._mostrar_lista_muebles(resultados)

    def filtrar_por_material_interactivo(self):
        """Interfaz interactiva para filtrar por material."""
        material = Prompt.ask("[green]🎨 Ingresa el material (ej: madera, metal, plástico)[/green]")
        if not material.strip():
            self.console.print("[red]❌ Material no puede estar vacío.[/red]")
            return
        with self.console.status(f"[bold green]Buscando muebles de {material}..."):
            time.sleep(0.3)
            resultados = self.tienda.filtrar_por_material(material)
        if not resultados:
            self.console.print(f"[yellow]❌ No hay muebles de material '{material}'.[/yellow]")
            return
        self.console.print(f"\n[green]✓ Muebles de {material}:[/green]")
        self._mostrar_lista_muebles(resultados)

    def mostrar_comedores(self):
        """Muestra todos los comedores disponibles."""
        comedores = self.tienda._comedores
        if not comedores:
            self.console.print("[yellow]No hay comedores disponibles.[/yellow]")
            return
        for i, comedor in enumerate(comedores, 1):
            panel = Panel(
                comedor.obtener_descripcion(),
                title=f"Comedor #{i}: {comedor.nombre}",
                border_style="green",
            )
            self.console.print(panel)

    def realizar_venta_interactiva(self):
        """Interfaz interactiva para realizar ventas."""
        muebles = self.tienda._inventario
        if not muebles:
            self.console.print("[red]No hay muebles disponibles para venta.[/red]")
            return
        self.console.print("[cyan]Selecciona un mueble para vender:[/cyan]")
        self._mostrar_lista_muebles(muebles, numerada=True)
        try:
            indice = IntPrompt.ask(
                "Número del mueble",
                choices=[str(i) for i in range(1, len(muebles) + 1)],
            )
            mueble_seleccionado = muebles[indice - 1]
            self.console.print("\n[green]Mueble seleccionado:[/green]")
            self.console.print(mueble_seleccionado.obtener_descripcion())
            if not Confirm.ask("\n¿Confirmar la venta?"):
                self.console.print("[yellow]Venta cancelada.[/yellow]")
                return
            cliente = Prompt.ask("Nombre del cliente", default="Cliente Anónimo")
            resultado = self.tienda.realizar_venta(mueble_seleccionado, cliente)
            if "error" in resultado:
                self.console.print(f"[red]Error: {resultado['error']}[/red]")
            else:
                self._mostrar_comprobante_venta(resultado)
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida.[/red]")

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de la tienda."""
        with self.console.status("[bold green]Calculando estadísticas..."):
            time.sleep(0.5)
            stats = self.tienda.obtener_estadisticas()
        table = Table(title="📊 Estadísticas de la Tienda")
        table.add_column("Métrica", style="cyan", no_wrap=True)
        table.add_column("Valor", style="magenta", justify="right")
        table.add_row("Total de muebles", str(stats["total_muebles"]))
        table.add_row("Total de comedores", str(stats["total_comedores"]))
        table.add_row("Valor del inventario", f"${stats['valor_inventario']:.2f}")
        table.add_row("Ventas realizadas", str(stats["ventas_realizadas"]))
        table.add_row("Descuentos activos", str(stats["descuentos_activos"]))
        self.console.print(table)
        if stats["tipos_muebles"]:
            self.console.print("\n[cyan]Distribución por tipos:[/cyan]")
            for tipo, cantidad in stats["tipos_muebles"].items():
                self.console.print(f"  • {tipo}: {cantidad} unidades")

    def generar_reporte_interactivo(self):
        """Genera y muestra el reporte de inventario."""
        with self.console.status("[bold green]Generando reporte..."):
            time.sleep(1)
            reporte = self.tienda.generar_reporte_inventario()
        self.console.print(
            Panel(reporte, title="📋 Reporte de Inventario", border_style="blue", padding=(1, 2))
        )
        if Confirm.ask("¿Deseas guardar el reporte en un archivo?"):
            filename = Prompt.ask("Nombre del archivo", default="reporte_inventario.txt")
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(reporte)
                self.console.print(f"[green]Reporte guardado en {filename}[/green]")
            except Exception as e:
                self.console.print(f"[red]Error al guardar: {str(e)}[/red]")

    def aplicar_descuentos_interactivo(self):
        """Interfaz para aplicar descuentos por categoría."""
        categorias = ["silla", "mesa", "sofa", "cama", "armario",
                      "escritorio", "cajonera", "sillon", "sofacama"]
        self.console.print("[cyan]Categorías disponibles:[/cyan]")
        for i, cat in enumerate(categorias, 1):
            self.console.print(f"  {i}. {cat.title()}")
        try:
            indice = IntPrompt.ask(
                "Selecciona una categoría",
                choices=[str(i) for i in range(1, len(categorias) + 1)],
            )
            categoria = categorias[indice - 1]
            porcentaje = IntPrompt.ask(
                f"Porcentaje de descuento para {categoria}s (1-50)",
                choices=[str(i) for i in range(1, 51)],
            )
            resultado = self.tienda.aplicar_descuento(categoria, porcentaje)
            self.console.print(f"[green]{resultado}[/green]")
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida.[/red]")

    def _mostrar_lista_muebles(self, muebles: List[Mueble], numerada: bool = False):
        """Muestra una lista de muebles en formato tabla."""
        table = Table()
        if numerada:
            table.add_column("#", style="cyan", no_wrap=True)
        table.add_column("Nombre", style="magenta")
        table.add_column("Tipo", style="green")
        table.add_column("Material", style="yellow")
        table.add_column("Color", style="blue")
        table.add_column("Precio", style="red", justify="right")
        for i, mueble in enumerate(muebles, 1):
            try:
                precio = f"${mueble.calcular_precio():.2f}"
                tipo = type(mueble).__name__
                row = [mueble.nombre, tipo, mueble.material, mueble.color, precio]
                if numerada:
                    row.insert(0, str(i))
                table.add_row(*row)
            except Exception:
                row = [mueble.nombre, "Error", mueble.material, mueble.color, "Error"]
                if numerada:
                    row.insert(0, str(i))
                table.add_row(*row)
        self.console.print(table)

    def _mostrar_comprobante_venta(self, venta: dict):
        """Muestra el comprobante de venta."""
        comprobante = (
            f"Cliente: {venta.get('cliente', 'N/A')}\n"
            f"Producto: {venta.get('mueble', 'N/A')}\n"
            f"Precio original: ${venta.get('precio_original', 0):.2f}\n"
            f"Descuento aplicado: {venta.get('descuento', 0):.1f}%\n"
            f"PRECIO FINAL: ${venta.get('precio_final', 0):.2f}\n\n"
            "¡Gracias por su compra!"
        )
        self.console.print(
            Panel(comprobante, title="🧾 Venta Exitosa", border_style="green", padding=(1, 2))
        )

    def ejecutar(self):
        """Ejecuta el bucle principal del menú."""
        self.console.clear()
        self.mostrar_banner()
        acciones = {
            1: self.mostrar_catalogo_completo,
            2: self.buscar_muebles_interactivo,
            3: self.filtrar_por_precio_interactivo,
            4: self.filtrar_por_material_interactivo,
            5: self.mostrar_comedores,
            6: self.realizar_venta_interactiva,
            7: self.mostrar_estadisticas,
            8: self.generar_reporte_interactivo,
            9: self.aplicar_descuentos_interactivo,
        }
        while self.running:
            try:
                opcion = self.mostrar_menu_principal()
                if opcion == 0:
                    self.console.print("[bold green]¡Hasta luego! 👋[/bold green]")
                    self.running = False
                elif opcion in acciones:
                    acciones[opcion]()
                if self.running:
                    input("\nPresiona Enter para continuar...")
                    self.console.clear()
            except KeyboardInterrupt:
                self.console.print("\n[red]Operación cancelada.[/red]")
                self.running = False
            except Exception as e:
                self.console.print(f"[red]Error inesperado: {str(e)}[/red]")
                input("Presiona Enter para continuar...")
