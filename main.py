# main.py

# --- IMPORTACIÓN DE MÓDULOS ---
# 1. Importar gestor_ingredientes PRIMERO. 
#    Esto carga el 'dict_ingredientes_maestro'.
import gestor_ingredientes

# 2. Importar gestor_menu DESPUÉS. 
#    Ahora puede importar el dict de ingredientes de forma segura.
import gestor_menu

# Importamos las CLASES y FUNCIONES necesarias
from gestor_inventario import GestorInventario
import simulador_ventas 

# --- INSTANCIACIÓN DE OBJETOS ---
# ✅ Se inyecta el catálogo (ahora en minúsculas) en el inventario.
gestor_inventario_inst = GestorInventario(
    catalogo_ingredientes=gestor_ingredientes.dict_ingredientes_maestro
)

# --- DEFINICIÓN DE SUB-MENÚS (HANDLERS) ---

def validacion_opcion(opcion):
    """Valida que la opción sea un número entre 1 y 6."""
    if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 6:
        print("❌ Opción inválida. Intente de nuevo (1-6).")
        return False
    return True

def manejar_gestion_ingredientes():
        """Muestra el sub-menú y maneja las opciones del Módulo 1."""
        print("\n[Módulo 1: Gestión de Ingredientes]")
        print("1. Listar ingredientes por categoría")
        print("2. Listar un tipo de ingrediente específico")
        print("3. Agregar nuevo ingrediente (No implementado)")
        print("4. Eliminar ingrediente")
        print("5. Volver al menú principal")
        op = input("--> ")
        
        if op == "1":
            gestor_ingredientes.listar_productos_categoria()
        elif op == "2":
            gestor_ingredientes.listar_productos_categoria_tipo()
        elif op == "3":
            gestor_ingredientes.agregar_ingrediente()
        elif op == "4":
            gestor_ingredientes.eliminar_ingrediente_interactivo()
        elif op == "5":
            return
        else:
            print("❌ Opción inválida.")

def manejar_gestion_inventario():
        """Muestra el sub-menú y maneja las opciones del Módulo 2."""
        print("\n[Módulo 2: Gestión de Inventario]")
        print("1. Visualizar todo el inventario")
        print("2. Buscar existencia de un ingrediente")
        print("3. Listar existencias por categoría")
        print("4. Actualizar existencia (Añadir/Quitar Stock)")
        print("5. Volver al menú principal")
        op = input("--> ")
        
        if op == "1":
            gestor_inventario_inst.visualizar_inventario()
        elif op == "2":
            gestor_inventario_inst.buscar_existencia_especifica()
        elif op == "3":
            gestor_inventario_inst.listar_existencias_por_categoria()
        elif op == "4":
            gestor_inventario_inst.actualizar_existencia_interactivo()
        elif op == "5":
            return
        else:
            print("❌ Opción inválida.")
            
def manejar_gestion_menu():
    """Muestra el sub-menú y maneja las opciones del Módulo 3."""
    print("\n[Módulo 3: Gestión del Menú]")
    print("1. Listar HotDogs en el menú")
    print("2. Agregar un HotDog al menú")
    print("3. Eliminar un HotDog del menú")
    print("4. Volver al menú principal")
    op = input("--> ")
    
    # 'menu' es una lista: [dict_hotdogs, list_combos]
    # Accedemos al dict de hotdogs en el índice [0]
    if not gestor_menu.menu or not isinstance(gestor_menu.menu, list):
        print("❌ Error fatal: El menú no se cargó. Revise las dependencias.")
        return
        
    menu_actual = gestor_menu.menu[0] 
    
    if op == "1":
        # Esta llamada ahora es segura
        gestor_menu.listar_hotdogs(menu_actual)
    elif op == "2":
        # ✅ Se pasan los 3 argumentos que la función espera
        gestor_menu.agregar_hotdog_interactivo(
            menu_actual, 
            gestor_menu.guardar_datos_menu, 
            gestor_ingredientes.dict_ingredientes_maestro # Se pasa el catálogo
        )
    elif op == "3":
        nombre_hd = input("▶️ Ingrese el nombre del HotDog a eliminar: ").strip()
        gestor_menu.eliminar_hotdog(menu_actual, gestor_menu.guardar_datos_menu, nombre_hd)
    elif op == "4":
        return
    else:
        print("❌ Opción inválida.")


def main():
    """Función principal del programa."""
    
    historial_simulaciones = simulador_ventas.cargar_datos_locales()
    
    while True:
        print("\n" + "="*40)
        print("🌭 SISTEMA DE GESTIÓN DE HOT DOGS 🌭")
        print("="*40)
        print("1. Gestión de Ingredientes")
        print("2. Gestión de Inventario")
        print("3. Gestión del Menú")
        print("4. Simular un Día de Ventas")
        print("5. Mostrar Estadísticas Históricas (Bono)")
        print("6. Salir")
            
        opcion = input("Seleccione una opción:\n---> ")
        
        if not validacion_opcion(opcion):
            continue

        if opcion == "1":
            manejar_gestion_ingredientes()
        elif opcion == "2":
            manejar_gestion_inventario()
        elif opcion == "3":
            manejar_gestion_menu()
        elif opcion == "4":
            historial_simulaciones = simulador_ventas.simular_dia(
                gestor_menu=gestor_menu.menu[0], # Pasa solo el dict de hotdogs
                gestor_inventario=gestor_inventario_inst, 
                gestor_ingredientes=gestor_ingredientes.dict_ingredientes_maestro,
                historial_simulaciones=historial_simulaciones
            )
        elif opcion == "5":
            simulador_ventas.mostrar_estadisticas_historicas(historial_simulaciones)
        elif opcion == "6":
            print("\n👋 ¡Hasta luego! Guardando y cerrando el sistema...")
            break
        
if __name__ == "__main__":
    main()
    #
