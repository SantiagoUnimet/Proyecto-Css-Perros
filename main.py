# ----------------------------------------------------------------------
# Aplicación Principal - Hot Dog CCS
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

# Variables globales de los gestores
g_ingredientes = None
g_inventario = None
g_menu = None
g_simulador = None
g_stats = None


# --- Helpers de Creación (NUEVAS FUNCIONES PARA MÓDULO 1.3) ---

def _crear_ingrediente_tipo_1(categoria):
    """
    Crea Pan, Salchicha, o Acompañante, ya que tienen los
    mismos atributos: (nombre, tipo, tamaño, unidad).
    """
    print(f"\n--- Creando nuevo ingrediente: {categoria} ---")
    nombre = utils.validar_input_texto("Nombre: ")
    
    # Chequear duplicado antes de pedir más datos
    if g_ingredientes.buscar_ingrediente(nombre):
        print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
        return

    tipo = utils.validar_input_texto("Tipo (ej: Blanco, Res, Bebida): ")
    # Usamos float para permitir decimales en tamaño/unidad
    tamaño = utils.validar_input_numerico("Tamaño (ej: 6, 200, 350): ", tipo_dato=float, rango=[1, 5000])
    unidad = utils.validar_input_texto("Unidad (ej: pulgadas, gramos, ml): ")
    
    # Crear el objeto de la clase correcta
    nuevo = None
    if categoria == "Pan":
        nuevo = Pan(categoria, nombre, tipo, tamaño, unidad)
    elif categoria == "Salchicha":
        nuevo = Salchicha(categoria, nombre, tipo, tamaño, unidad)
    elif categoria == "Acompañante":
        nuevo = Acompañante(categoria, nombre, tipo, tamaño, unidad)
    
    # Agregar al gestor
    if nuevo:
        g_ingredientes.agregar_ingrediente(nuevo)

def _crear_salsa():
    """Crea una Salsa (nombre, base, color)."""
    print("\n--- Creando nuevo ingrediente: Salsa ---")
    nombre = utils.validar_input_texto("Nombre: ")
    if g_ingredientes.buscar_ingrediente(nombre):
        print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
        return

    base = utils.validar_input_texto("Base (ej: Tomate, Aceite): ")
    color = utils.validar_input_texto("Color (ej: Rojo, Blanco): ")
    
    nuevo = Salsa("Salsa", nombre, base, color)
    g_ingredientes.agregar_ingrediente(nuevo)

def _crear_topping():
    """Crea un Topping (nombre, tipo, presentacion)."""
    print("\n--- Creando nuevo ingrediente: Topping ---")
    nombre = utils.validar_input_texto("Nombre: ")
    if g_ingredientes.buscar_ingrediente(nombre):
        print(f"Error: Ya existe un ingrediente con el nombre '{nombre}'. Creación cancelada.")
        return

    tipo = utils.validar_input_texto("Tipo (ej: Vegetal, Fritura): ")
    # El JSON de la API usa 'presentación' con acento
    presentacion = utils.validar_input_texto("Presentación (ej: Cuadritos, Rallado): ")
    
    nuevo = Topping("Topping", nombre, tipo, presentacion)
    g_ingredientes.agregar_ingrediente(nuevo)


# --- Sub-menús de Módulos ---

# (Puedes pegar esto justo después de la función _crear_topping())

def _seleccionar_ingrediente(categoria, permitir_ninguno=False):
    """
    Muestra una lista de ingredientes de una categoría y pide al usuario
    que seleccione uno. Retorna el objeto ingrediente.
    """
    print(f"\n--- Seleccionar {categoria} ---")
    
    # Obtener la lista de ingredientes de esa categoría
    lista_ing = g_ingredientes._ingredientes_por_categoria.get(categoria, [])
    
    if not lista_ing:
        print(f"Error: No hay ingredientes registrados en la categoría '{categoria}'.")
        return None 
        
    # Imprimir la lista numerada
    for i, ing in enumerate(lista_ing):
        print(f"{i+1}. {ing.get_nombre()}") # Muestra (ej: "1. simple")
    
    # Configurar el prompt y el rango de opciones válidas
    if permitir_ninguno:
        print("0. Ninguno")
        prompt = "Seleccione un número (0 para ninguno): "
        rango = [0, len(lista_ing)]
    else:
        prompt = "Seleccione un número: "
        rango = [1, len(lista_ing)] # Rango obligatorio

    # Validar la selección del usuario
    opcion = utils.validar_input_numerico(prompt, rango=rango)

    if permitir_ninguno and opcion == 0:
        return None # El usuario eligió "Ninguno"
    
    # Retornar el objeto ingrediente seleccionado
    return lista_ing[opcion - 1]

def _seleccionar_multiples_ingredientes(categoria):
    """
    Permite al usuario seleccionar múltiples ingredientes de una categoría
    (para toppings y salsas).
    """
    seleccionados = []
    while True:
        # Reutilizamos la función anterior, permitiendo "Ninguno" para terminar
        ing = _seleccionar_ingrediente(categoria, permitir_ninguno=True)
        
        if ing is None: # El usuario seleccionó "0. Ninguno"
            break # Termina de agregar
            
        seleccionados.append(ing)
        print(f"'{ing.get_nombre()}' agregado.")
        
        # Preguntar si desea agregar otro
        if not utils.validar_confirmacion("¿Agregar otro ingrediente de esta categoría?"):
            break
            
    return seleccionados

def menu_modulo_1():
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
            g_ingredientes.listar_por_categoria(categoria)
        
        elif opcion == 2:
            categoria = input("Ingrese la categoría (Pan, Salchicha, Topping, Acompañante): ").capitalize()
            tipo = input(f"Ingrese el tipo a buscar en {categoria}: ")
            g_ingredientes.listar_por_tipo(categoria, tipo)

        elif opcion == 3:
            # --- ¡FUNCIÓN IMPLEMENTADA! ---
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
                _crear_ingrediente_tipo_1("Pan")
            elif cat_opcion == 2:
                _crear_ingrediente_tipo_1("Salchicha")
            elif cat_opcion == 3:
                _crear_topping()
            elif cat_opcion == 4:
                _crear_salsa()
            elif cat_opcion == 5:
                _crear_ingrediente_tipo_1("Acompañante")
            elif cat_opcion == 0:
                print("Creación cancelada.")

        elif opcion == 4:
            # Esta función ya estaba lista:
            nombre = input("Ingrese el nombre exacto del ingrediente a eliminar: ")
            g_ingredientes.eliminar_ingrediente(nombre, g_menu)

        elif opcion == 0:
            break

def menu_modulo_2():
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
            g_inventario.visualizar_todo()
        
        elif opcion == 2:
            nombre = input("Ingrese el nombre exacto del ingrediente: ")
            g_inventario.buscar_existencia(nombre)

        elif opcion == 3:
            categoria = input("Ingrese la categoría (Pan, Salchicha, Topping, Salsa, Acompañante): ").capitalize()
            g_inventario.listar_por_categoria(categoria)
            
        elif opcion == 4:
            nombre = input("Ingrese el nombre exacto del ingrediente a actualizar: ")
            cantidad = utils.validar_input_numerico(f"Ingrese la cantidad a AGREGAR a '{nombre}': ", tipo_dato=int, rango=[1, 10000])
            g_inventario.actualizar_existencia(nombre, cantidad)
            
        elif opcion == 0:
            break

def menu_modulo_3():
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
            g_menu.ver_lista_hotdogs()
            
        elif opcion == 2:
            nombre = input("Ingrese el nombre exacto del Hot Dog: ")
            g_menu.ver_inventario_para_hotdog(nombre, g_inventario)

        elif opcion == 3:
            # --- ¡FUNCIÓN IMPLEMENTADA! ---
            print("\n--- Agregar Nuevo Hot Dog ---")
            nombre = utils.validar_input_texto("Nombre del nuevo Hot Dog: ")
            if g_menu.buscar_hotdog(nombre):
                print(f"Error: Ya existe un hot dog con el nombre '{nombre}'. Creación cancelada.")
                continue # Vuelve al menú del Módulo 3

            # 1. Seleccionar Pan (Obligatorio)
            pan_obj = _seleccionar_ingrediente("Pan")
            if pan_obj is None: # Ocurre si no hay panes registrados
                print("Creación cancelada.")
                continue
            
            # 2. Seleccionar Salchicha (Obligatorio)
            salchicha_obj = _seleccionar_ingrediente("Salchicha")
            if salchicha_obj is None: # Ocurre si no hay salchichas registradas
                print("Creación cancelada.")
                continue
            
            # 3. Seleccionar Toppings (Opcional, múltiple)
            toppings_lista = _seleccionar_multiples_ingredientes("Topping")
            
            # 4. Seleccionar Salsas (Opcional, múltiple)
            salsas_lista = _seleccionar_multiples_ingredientes("Salsa")
            
            # 5. Seleccionar Acompañante (Opcional, singular)
            print("\n(Opcional) Seleccione un Acompañante para el combo:")
            acomp_obj = _seleccionar_ingrediente("Acompañante", permitir_ninguno=True)
            
            # 6. Crear y agregar el nuevo Hot Dog
            nuevo_hd = HotDog(nombre, pan_obj, salchicha_obj, toppings_lista, salsas_lista, acomp_obj)
            
            # 7. Usar la función del gestor (que ya valida compatibilidad e inventario)
            g_menu.agregar_hotdog(nuevo_hd, g_inventario) 

        elif opcion == 4:
            nombre = input("Ingrese el nombre exacto del Hot Dog a eliminar: ")
            g_menu.eliminar_hotdog(nombre, g_inventario)
            
        elif opcion == 0:
            break

def menu_modulo_5():
    """Maneja la UI del Módulo 5: Simulación."""
    print("\n--- Módulo 5: Simular un Día de Ventas ---")
    if utils.validar_confirmacion("¿Está seguro de que desea simular un día? Esto modificará el inventario."):
        reporte = g_simulador.simular_dia()
        if reporte:
            g_stats.agregar_reporte(reporte)
            print("\nSimulación completada y reporte guardado en estadísticas.")
    else:
        print("Simulación cancelada.")

# --- Funciones Principales de Arranque y Cierre ---

def inicializar_sistema():
    """Descarga datos API, carga datos locales e inicializa los gestores."""
    global g_ingredientes, g_inventario, g_menu, g_simulador, g_stats
    
    api_ing, api_menu = utils.descargar_datos_api()
    if api_ing is None or api_menu is None:
        return False 
        
    datos_locales = utils.cargar_datos_locales()
    
    g_ingredientes = GestorIngredientes()
    g_inventario = GestorInventario(g_ingredientes)
    g_menu = GestorMenu(g_ingredientes)
    g_stats = GestorEstadisticas()
    
    # Cargar datos en los Gestores
    
    # --- ¡MODIFICADO! ---
    # Pasamos la lista negra a los cargadores de la API
    g_ingredientes.cargar_ingredientes_api(
        api_ing, 
        datos_locales["api_ingredientes_eliminados"]
    )
    g_ingredientes.cargar_ingredientes_locales(
        datos_locales["nuevos_ingredientes"]
    )
    
    g_inventario.cargar_inventario_local(datos_locales["inventario"])
    
    # --- ¡MODIFICADO! ---
    g_menu.cargar_menu_api(
        api_menu, 
        datos_locales["api_hotdogs_eliminados"]
    )
    g_menu.cargar_menu_local(datos_locales["nuevos_hotdogs"])
    
    g_stats.cargar_estadisticas(datos_locales["estadisticas"])

    g_simulador = Simulador(g_menu, g_inventario, g_ingredientes)
    
    print("\n¡Sistema Hot Dog CCS inicializado y listo!")
    return True

def guardar_y_salir():
    """Guarda el estado actual en el archivo JSON local."""
    print("Guardando datos...")
    
    datos_a_guardar = {
        "nuevos_ingredientes": g_ingredientes.get_ingredientes_para_guardar(),
        "nuevos_hotdogs": g_menu.get_menu_para_guardar(),
        "inventario": g_inventario.get_inventario_para_guardar(),
        "estadisticas": g_stats.get_estadisticas_para_guardar(),
        "api_ingredientes_eliminados": g_ingredientes.get_api_eliminados_para_guardar(), # NUEVO
        "api_hotdogs_eliminados": g_menu.get_api_eliminados_para_guardar()              # NUEVO
    }
    
    utils.guardar_datos_locales(datos_a_guardar)
    print("¡Gracias por usar Hot Dog CCS! Adiós.")
    sys.exit()

# --- Bucle Principal ---

def main():
    if not inicializar_sistema():
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
            menu_modulo_1()
        elif opcion == 2:
            menu_modulo_2()
        elif opcion == 3:
            menu_modulo_3()
        elif opcion == 5:
            menu_modulo_5()
        elif opcion == 6:
            g_stats.mostrar_estadisticas()
        elif opcion == 0:
            guardar_y_salir()

main()
