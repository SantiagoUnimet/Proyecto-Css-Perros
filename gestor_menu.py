class GestorMenu:
    """
    Módulo para la gestión de las opciones de Hot Dog disponibles (Módulo 3).
    """
    def __init__(self):
        self._menu_hotdogs = {}
        self._datos_locales_ruta = "datos_locales_menu.json"

    # Métodos de Persistencia
    def cargar_datos_locales(self, gestor_ingredientes):
        try:
            with open(self._datos_locales_ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                for data in datos:
                    pan_obj = gestor_ingredientes.get_ingredientes_maestros().get(data.get('pan'))
                    salchicha_obj = gestor_ingredientes.get_ingredientes_maestros().get(data.get('salchicha'))
                    
                    toppings_objs = [gestor_ingredientes.get_ingredientes_maestros().get(t) for t in data.get('toppings', []) if gestor_ingredientes.get_ingredientes_maestros().get(t)]
                    salsas_objs = [gestor_ingredientes.get_ingredientes_maestros().get(s) for s in data.get('salsas', []) if gestor_ingredientes.get_ingredientes_maestros().get(s)]
                    
                    acompanante_obj = gestor_ingredientes.get_ingredientes_maestros().get(data.get('acompanante_combo')) if data.get('acompanante_combo') else None
                    
                    if pan_obj and salchicha_obj:
                        nuevo_hotdog = HotDog(
                            nombre=data['nombre'],
                            pan=pan_obj,
                            salchicha=salchicha_obj,
                            toppings=toppings_objs,
                            salsas=salsas_objs,
                            acompanante_combo=acompanante_obj
                        )
                        self._menu_hotdogs[data['nombre']] = nuevo_hotdog
                        
                print(f"✅ {len(self._menu_hotdogs)} Hot Dogs cargados desde {self._datos_locales_ruta}.")
                
        except FileNotFoundError:
            print("ℹ️ No se encontró archivo de menú local. Iniciando vacío o con datos por defecto.")
        except json.JSONDecodeError:
            print("❌ Error al decodificar el archivo JSON del menú.")

    def guardar_datos_locales(self):
        """Guarda los Hot Dogs actuales en un archivo JSON."""
        datos_a_guardar = [hd.to_dict() for hd in self._menu_hotdogs.values()]
        
        try:
            with open(self._datos_locales_ruta, 'w', encoding='utf-8') as f:
                json.dump(datos_a_guardar, f, indent=4)
        except Exception as e:
            print(f"❌ Error al guardar el menú: {e}")

    # Métodos de Gestión
    def ver_lista_hotdogs(self):
        """Muestra la lista de Hot Dogs actualmente en el menú."""
        print("\n--- Menú Actual de Hot Dogs ---")
        if not self._menu_hotdogs:
            print("El menú está vacío.")
            return

        for nombre in self._menu_hotdogs.keys():
            print(f"- {nombre}")

    def agregar_hotdog(self, hotdog, gestor_inventario):
        """Agrega un HotDog, realizando validaciones de longitud y existencia de inventario."""
        nombre = hotdog.get_nombre()
        if nombre in self._menu_hotdogs:
            print("❌ Error: Ese HotDog ya existe.")
            return

        # 1. Validación de Longitud (Pan vs. Salchicha) - Lógica de confirmación
        if hotdog._pan and hotdog._salchicha and not hotdog._pan.es_compatible(hotdog._salchicha):
            print("⚠️ Advertencia de Longitud:")
            print(f"El Pan ({hotdog._pan._tamaño} cm) y la Salchicha ({hotdog._salchicha._tamaño} cm) NO coinciden.")
            
            respuesta = input("¿Desea crear este HotDog a pesar de la incompatibilidad de tamaño? (S/N): ").strip().upper()

            if respuesta != 'S':
                print(f"🚫 Creación de HotDog '{nombre}' cancelada por el usuario.")
                return

        # 2. Validación de Inventario (Advertencia)
        if not hotdog.validar_inventario(gestor_inventario):
            print("⚠️ Advertencia de Inventario: No hay inventario suficiente para este HotDog en este momento.")
        
        # 3. Guardar el nuevo HotDog
        self._menu_hotdogs[nombre] = hotdog
        self.guardar_datos_locales()
        print(f"✅ HotDog '{nombre}' agregado al menú.")

    def eliminar_hotdog(self, nombre, gestor_inventario):
        """Elimina un HotDog."""
        if nombre not in self._menu_hotdogs:
            return
        
        del self._menu_hotdogs[nombre]
        self.guardar_datos_locales()
        print(f"✅ HotDog '{nombre}' eliminado del menú.")
        
    def get_menu(self):
        return self._menu_hotdogs
