

# ----------------------------------------------------------------------
# 3. Clase Coordinadora (Sistema)
# ----------------------------------------------------------------------

 """
Clase principal que coordina el sistema y los módulos.
"""
def __init__(self):
    """Inicializa todos los gestores y carga los datos iniciales (Composición)."""
    # Atributos privados (-) - Referencias a otros Gestores (Composición)
    self._gestor_ingredientes_ref = GestorIngredientes()
    self._gestor_menu_ref = GestorMenu()
    self._gestor_inventario_ref = GestorInventario()
    self._simulador_ventas_ref = SimuladorVentas()
    
    # Cargar datos al iniciar
    self._gestor_ingredientes_ref.cargar_datos_api()
    self._gestor_ingredientes_ref.cargar_datos_locales()
    self._gestor_inventario_ref.cargar_datos_locales()
    self._gestor_menu_ref.cargar_datos_locales(self._gestor_ingredientes_ref)
    self._simulador_ventas_ref.cargar_datos_locales()
# Métodos de Utilidad (Validación de Entrada)
def obtener_numero_valido( mensaje, tipo_esperado=int):
    """Pide entrada al usuario y la valida contra el tipo esperado (int o float)."""
    while True:
        try:
            entrada = input(mensaje)
            valor = tipo_esperado(entrada)
            
            if valor < 0:
                print("❌ Error: Por favor, ingrese un número no negativo.")
                continue
                
            return valor
        
        except ValueError:
            print("❌ Error de entrada: Por favor, ingrese un valor del tipo numérico esperado.")
        
def obtener_opcion_valida(self, mensaje, opciones_validas):
     """Obtiene una opción de menú validada contra una lista de opciones permitidas."""
     while True:
         opcion = obtener_numero_valido(mensaje, int)
         if opcion in opciones_validas:
             return opcion
         else:
             print("❌ Error: Opción no válida. Inténtelo de nuevo.")
 # Métodos Públicos
def iniciar_principal():
     """Inicia el bucle principal del programa y el menú de usuario."""
     print("\n==========================================")
     print(" Sistema HotDog CCS iniciado. ¡Bienvenido! 🌭")
     print("==========================================")
     
     while True:
         print("\n--- Menú Principal ---")
         print("1. Gestión de Ingredientes")
         print("2. Gestión de Inventario")
         print("3. Gestión del Menú")
         print("4. Simular un Día de Ventas")
         print("5. Mostrar Estadísticas Históricas (Bono)")
         print("6. Salir")
         
         
         opcion = input("Seleccione una opción:\n---> ")
         if opcion == "1":
             self.manejar_gestion_ingredientes()
         elif opcion == "2":
             self.manejar_gestion_inventario()
         elif opcion == "3":
             self.manejar_gestion_menu()
         elif opcion == "4":
             self._simulador_ventas_ref.simular_dia(self._gestor_menu_ref, self._gestor_inventario_ref, self._gestor_ingredientes_ref)
         elif opcion == "5":
             self._simulador_ventas_ref.mostrar_estadisticas_historicas()
         elif opcion == "6":
             print("¡Gracias por usar Hot Dog CCS! Guardando estado y saliendo.")
             break
 # Métodos de sub-menús (Ahora llaman a las funciones de listado para demostrar la funcionalidad)
def manejar_gestion_ingredientes():
        print("\n[Módulo 1: Gestión de Ingredientes]")
        
        # Aquí iría el sub-menú completo para añadir/eliminar/listar
        
def manejar_gestion_inventario():
        print("\n[Módulo 2: Gestión de Inventario]")
       
        # Aquí iría el sub-menú completo para visualizar o actualizar existencias
        
def manejar_gestion_menu():
        print("\n[Módulo 3: Gestión del Menú]")
        
        # Aquí iría el sub-menú completo para crear/eliminar/listar Hot Dogs
    