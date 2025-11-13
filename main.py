
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
    

# Esta función principal será el punto de entrada

def validacion_opcion(opcion):
     opcion_validas = ["1","2","3","4","5","6"]
     if opcion in opcion_validas:
          pass
     else:

         print("❌ Error: Opción no válida. Inténtelo de nuevo.")
         
    

def main():
    
    """Inicia el bucle principal del programa y el menú de usuario.
        """
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
        validacion_opcion(opcion)


        if opcion == "1":
            manejar_gestion_ingredientes()
        elif opcion == "2":
            manejar_gestion_inventario()
        elif opcion == "3":
            manejar_gestion_menu()
        elif opcion == "4":
            simulador_ventas_ref.simular_dia(self._gestor_menu_ref, self._gestor_inventario_ref, self._gestor_ingredientes_ref)
        elif opcion == "5":
            simulador_ventas_ref.mostrar_estadisticas_historicas()
        elif opcion == "6":
            print("¡Gracias por usar Hot Dog CCS! Guardando estado y saliendo.")
            break
     

    

main()

