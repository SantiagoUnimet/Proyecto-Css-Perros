# ----------------------------------------------------------------------
# Módulo Principal. Main
# ----------------------------------------------------------------------

import sys
import utils
from ingredientes import *
from hotdogs import HotDog
from gestor_ingredientes import GestorIngredientes
from gestor_inventario import GestorInventario
from gestor_menu import GestorMenu
from simulacion import Simulador
from estadisticas import GestorEstadisticas


class Aplicacion:
    """
    Clase principal que encapsula toda la lógica y el estado del programa.
    Reemplaza el uso de variables globales.
    """
    def __init__(self):
        self.URL_INGREDIENTES = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/ingredientes.json"
        self.URL_MENU = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"
        self.ARCHIVO_LOCAL = "hotdog_ccs_local.json"
        self.g_ingredientes = None
        self.g_inventario = None
        self.g_menu = None
        self.g_simulador = None
        self.g_stats = None

    
    def inicializar_sistema(self):
        """Descarga datos API, carga datos locales e inicializa los gestores."""
        api_ing, api_menu = utils.descargar_datos_api(
            self.URL_INGREDIENTES, 
            self.URL_MENU
        )
        if api_ing is None or api_menu is None:
            return False     
        datos_locales = utils.cargar_datos_locales(self.ARCHIVO_LOCAL)
        self.g_ingredientes = GestorIngredientes()
        self.g_inventario = GestorInventario(self.g_ingredientes)
        self.g_menu = GestorMenu(self.g_ingredientes)
        self.g_stats = GestorEstadisticas()
        self.g_ingredientes.cargar_ingredientes_api(
            api_ing, 
            datos_locales["api_ingredientes_eliminados"]
        )
        self.g_ingredientes.cargar_ingredientes_locales(
            datos_locales["nuevos_ingredientes"]
        )
        self.g_inventario.cargar_inventario_local(datos_locales["inventario"])
        self.g_menu.cargar_menu_api(
            api_menu, 
            datos_locales["api_hotdogs_eliminados"]
        )
        self.g_menu.cargar_menu_local(datos_locales["nuevos_hotdogs"])
        self.g_stats.cargar_estadisticas(datos_locales["estadisticas"])
        self.g_simulador = Simulador(
            self.g_menu, 
            self.g_inventario, 
            self.g_ingredientes
        )
        print("\n¡Sistema Hot Dog CCS inicializado y listo!")
        return True


    def guardar_y_salir(self):
        """Guarda el estado actual en el archivo JSON local."""
        print("Guardando datos...")
        datos_a_guardar = {
            "nuevos_ingredientes": self.g_ingredientes.get_ingredientes_para_guardar(),
            "nuevos_hotdogs": self.g_menu.get_menu_para_guardar(),
            "inventario": self.g_inventario.get_inventario_para_guardar(),
            "estadisticas": self.g_stats.get_estadisticas_para_guardar(),
            "api_ingredientes_eliminados": self.g_ingredientes.get_api_eliminados_para_guardar(),
            "api_hotdogs_eliminados": self.g_menu.get_api_eliminados_para_guardar()
        }
        utils.guardar_datos_locales(datos_a_guardar, self.ARCHIVO_LOCAL)
        print("¡Gracias por usar Hot Dog CCS! Adiós.")
        sys.exit()
    
    
    def _crear_ingrediente_tipo_1(self, categoria):
        """
        Crea Pan, Salchicha, o Acompañante, ya que tienen los
        mismos atributos: (nombre, tipo, tamaño, unidad).
        """
        print(f"\n--- Creando nuevo ingrediente: {categoria} ---")
        nombre = utils.validar_input_texto("Nombre: ")
        if self.g_ingredientes.buscar_ingrediente(nombre):
            print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
            return
        tipo = utils.validar_input_texto("Tipo (ej: Blanco, Res, Bebida): ")
        tamaño = utils.validar_input_numerico("Tamaño (ej: 6, 200, 350): ", tipo_dato=float, rango=[1, 5000])
        unidad = utils.validar_input_texto("Unidad (ej: pulgadas, gramos, ml): ")
        nuevo = None
        if categoria == "Pan":
            nuevo = Pan(categoria, nombre, tipo, tamaño, unidad)
        elif categoria == "Salchicha":
            nuevo = Salchicha(categoria, nombre, tipo, tamaño, unidad)
        elif categoria == "Acompañante":
            nuevo = Acompañante(categoria, nombre, tipo, tamaño, unidad)
        
        if nuevo:
            self.g_ingredientes.agregar_ingrediente(nuevo)


    def _crear_salsa(self):
        """Crea una Salsa (nombre, base, color)."""
        print("\n--- Creando nuevo ingrediente: Salsa ---")
        nombre = utils.validar_input_texto("Nombre: ")
        if self.g_ingredientes.buscar_ingrediente(nombre):
            print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
            return
        base = utils.validar_input_texto("Base (ej: Tomate, Aceite): ")
        color = utils.validar_input_texto("Color (ej: Rojo, Blanco): ")
        nuevo = Salsa("Salsa", nombre, base, color)
        self.g_ingredientes.agregar_ingrediente(nuevo)


    def _crear_topping(self):
        """Crea un Topping (nombre, tipo, presentacion)."""
        print("\n--- Creando nuevo ingrediente: Topping ---")
        nombre = utils.validar_input_texto("Nombre: ")
        if self.g_ingredientes.buscar_ingrediente(nombre):
            print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
            return
        tipo = utils.validar_input_texto("Tipo (ej: Vegetal, Fritura): ")
        presentacion = utils.validar_input_texto("Presentación (ej: Cuadritos, Rallado): ")
        nuevo = Topping("Topping", nombre, tipo, presentacion)
        self.g_ingredientes.agregar_ingrediente(nuevo)


    def _seleccionar_ingrediente(self, categoria, permitir_ninguno=False):
        """
        Muestra una lista de ingredientes de una categoría y pide al usuario
        que seleccione uno. Retorna el objeto ingrediente.
        """
        print(f"\n--- Seleccionar {categoria} ---")
        lista_ing = self.g_ingredientes._ingredientes_por_categoria.get(categoria, [])
        if not lista_ing:
            print(f"Error: No hay ingredientes registrados en la categoría '{categoria}'.")
            return None 
        for i, ing in enumerate(lista_ing):
            print(f"{i+1}. {ing.get_nombre()}")
        if permitir_ninguno:
            print("0. Ninguno")
            prompt = "Seleccione un número (0 para ninguno): "
            rango = [0, len(lista_ing)]
        else:
            prompt = "Seleccione un número: "
            rango = [1, len(lista_ing)]
        opcion = utils.validar_input_numerico(prompt, rango=rango)
        if permitir_ninguno and opcion == 0:
            return None
        return lista_ing[opcion - 1]


    def _seleccionar_multiples_ingredientes(self, categoria):
        """
        Permite al usuario seleccionar múltiples ingredientes de una categoría
        (para toppings y salsas).
        """
        seleccionados = []
        while True:
            ing = self._seleccionar_ingrediente(categoria, permitir_ninguno=True)
            if ing is None:
                break
            seleccionados.append(ing)
            print(f"'{ing.get_nombre()}' agregado.")
            
            if not utils.validar_confirmacion("¿Agregar otro ingrediente de esta categoría?"):
                break
        return seleccionados

    # --- MÉTODOS DE MENÚ ---

    def menu_modulo_1(self):
        """Maneja la UI del Módulo 1: Gestión de Ingredientes."""
        while True:
            print("\n--- Módulo 1: Gestión de Ingredientes ---")
            print("1. Listar ingredientes por categoría")
            print("2. Listar ingredientes por tipo (en una categoría)")
            print("3. Agregar nuevo ingrediente")
            print("4. Eliminar ingrediente")
            print("0. Volver al menú principal")
            opcion = utils.validar_input_numerico("Seleccione una opción: ", rango=[0, 4])
            if opcion == 1:
                categoria = input("Ingrese la categoría (Pan, Salchicha, Topping, Salsa, Acompañante): ").capitalize()
                self.g_ingredientes.listar_por_categoria(categoria)
            elif opcion == 2:
                categoria = input("Ingrese la categoría (Pan, Salchicha, Topping, Acompañante): ").capitalize()
                tipo = input(f"Ingrese el tipo a buscar en {categoria}: ")
                self.g_ingredientes.listar_por_tipo(categoria, tipo)
            elif opcion == 3:
                print("\n--- Agregar Nuevo Ingrediente ---")
                print("¿Qué categoría de ingrediente desea agregar?")
                print("1. Pan")
                print("2. Salchicha")
                print("3. Topping")
                print("4. Salsa")
                print("5. Acompañante")
                print("0. Cancelar")
                cat_opcion = utils.validar_input_numerico("Seleccione una categoría: ", rango=[0, 5])
                if cat_opcion == 1:
                    self._crear_ingrediente_tipo_1("Pan")
                elif cat_opcion == 2:
                    self._crear_ingrediente_tipo_1("Salchicha")
                elif cat_opcion == 3:
                    self._crear_topping()
                elif cat_opcion == 4:
                    self._crear_salsa()
                elif cat_opcion == 5:
                    self._crear_ingrediente_tipo_1("Acompañante")
                elif cat_opcion == 0:
                    print("Creación cancelada.")
            elif opcion == 4:
                nombre = input("Ingrese el nombre exacto del ingrediente a eliminar: ")
                self.g_ingredientes.eliminar_ingrediente(nombre, self.g_menu)
            elif opcion == 0:
                break
    

    def menu_modulo_2(self):
        """Maneja la UI del Módulo 2: Gestión de Inventario."""
        while True:
            print("\n--- Módulo 2: Gestión de Inventario ---")
            print("1. Visualizar todo el inventario")
            print("2. Buscar existencia de ingrediente específico")
            print("3. Listar existencias por categoría")
            print("4. Actualizar existencia (Comprar más)")
            print("0. Volver al menú principal")
            opcion = utils.validar_input_numerico("Seleccione una opción: ", rango=[0, 4])
            if opcion == 1:
                self.g_inventario.visualizar_todo()
            elif opcion == 2:
                nombre = input("Ingrese el nombre exacto del ingrediente: ")
                self.g_inventario.buscar_existencia(nombre)
            elif opcion == 3:
                categoria = input("Ingrese la categoría (Pan, Salchicha, Topping, Salsa, Acompañante): ").capitalize()
                self.g_inventario.listar_por_categoria(categoria) 
            elif opcion == 4:
                nombre = input("Ingrese el nombre exacto del ingrediente a actualizar: ")
                cantidad = utils.validar_input_numerico(f"Ingrese la cantidad a AGREGAR a '{nombre}': ", tipo_dato=int, rango=[1, 10000])
                self.g_inventario.actualizar_existencia(nombre, cantidad)
            elif opcion == 0:
                break

    
    def menu_modulo_3(self):
        """Maneja la UI del Módulo 3: Gestión del Menú."""
        while True:
            print("\n--- Módulo 3: Gestión del Menú ---")
            print("1. Ver lista de Hot Dogs")
            print("2. Verificar inventario para un Hot Dog")
            print("3. Agregar nuevo Hot Dog")
            print("4. Eliminar Hot Dog")
            print("0. Volver al menú principal")
            opcion = utils.validar_input_numerico("Seleccione una opción: ", rango=[0, 4])
            if opcion == 1:
                self.g_menu.ver_lista_hotdogs()
            elif opcion == 2:
                nombre = input("Ingrese el nombre exacto del Hot Dog: ")
                self.g_menu.ver_inventario_para_hotdog(nombre, self.g_inventario)
            elif opcion == 3:
                print("\n--- Agregar Nuevo Hot Dog ---")
                nombre = utils.validar_input_texto("Nombre del nuevo Hot Dog: ")
                if self.g_menu.buscar_hotdog(nombre):
                    print(f"Error: Ya existe un hot dog con el nombre '{nombre}'. Creación cancelada.")
                    continue
                pan_obj = self._seleccionar_ingrediente("Pan")
                if pan_obj is None:
                    print("Creación cancelada.")
                    continue
                salchicha_obj = self._seleccionar_ingrediente("Salchicha")
                if salchicha_obj is None:
                    print("Creación cancelada.")
                    continue
                toppings_lista = self._seleccionar_multiples_ingredientes("Topping")
                salsas_lista = self._seleccionar_multiples_ingredientes("Salsa")
                print("\n(Opcional) Seleccione un Acompañante para el combo:")
                acomp_obj = self._seleccionar_ingrediente("Acompañante", permitir_ninguno=True)
                nuevo_hd = HotDog(nombre, pan_obj, salchicha_obj, toppings_lista, salsas_lista, acomp_obj)
                self.g_menu.agregar_hotdog(nuevo_hd, self.g_inventario) 
            elif opcion == 4:
                nombre = input("Ingrese el nombre exacto del Hot Dog a eliminar: ")
                self.g_menu.eliminar_hotdog(nombre, self.g_inventario)
            elif opcion == 0:
                break
    

    def menu_modulo_5(self):
        """Maneja la UI del Módulo 5: Simulación."""
        print("\n--- Módulo 5: Simular un Día de Ventas ---")
        if utils.validar_confirmacion("¿Está seguro de que desea simular un día? Esto modificará el inventario."):
            reporte = self.g_simulador.simular_dia()
            if reporte:
                self.g_stats.agregar_reporte(reporte)
                print("\nSimulación completada y reporte guardado en estadísticas.")
        else:
            print("Simulación cancelada.")

    # --- MÉTODO PRINCIPAL DE EJECUCIÓN ---

    def iniciar_bucle_principal(self):
        """Inicia el bucle principal del menú de la aplicación."""
        if not self.inicializar_sistema():
            sys.exit("Error en la inicialización. Saliendo.")
        while True:
            print("\n--- Menú Principal: Hot Dog CCS ---")
            print("1. Gestión de Ingredientes (Módulo 1)")
            print("2. Gestión de Inventario (Módulo 2)")
            print("3. Gestión del Menú (Módulo 3)")
            print("5. Simular un Día de Ventas (Módulo 5)")
            print("6. Ver Estadísticas (Módulo Bonus)")
            print("0. Guardar y Salir")
            opcion = utils.validar_input_numerico("Seleccione una opción: ", rango=[0, 6])
            if opcion == 1:
                self.menu_modulo_1()
            elif opcion == 2:
                self.menu_modulo_2()
            elif opcion == 3:
                self.menu_modulo_3()
            elif opcion == 5:
                self.menu_modulo_5()
            elif opcion == 6:
                self.g_stats.mostrar_estadisticas()
            elif opcion == 0:
                self.guardar_y_salir()

# --- PUNTO DE ENTRADA DEL PROGRAMA ---

def main():
    """Función principal que crea e inicia la aplicación."""
    app = Aplicacion()
    app.iniciar_bucle_principal()

main()

