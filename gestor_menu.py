from hotdogs import HotDog
import json
import requests
import pickle


# Métodos de Persistencia
# En gestor_menu.py

# --- NUEVA FUNCIÓN DE BÚSQUEDA ---
def _buscar_ingrediente_por_nombre(nombre_ingrediente, dict_ingredientes):
    """Busca un objeto ingrediente en el diccionario maestro por su nombre."""
    if not nombre_ingrediente: # Si el nombre es None o ""
        return None
    for ing_obj in dict_ingredientes.values():
        if ing_obj.get_nombre() == nombre_ingrediente:
            return ing_obj
    print(f"Advertencia: No se encontró el objeto ingrediente para '{nombre_ingrediente}'")
    return None

def obtener_datos_menu(dict_ingredientes): # <-- AÑADIR PARÁMETRO
    """Descarga y carga los datos iniciales de la API de GitHub."""
    
    api_menu = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"
    response = requests.get(api_menu)
    menu = {} # El menú será un diccionario de {nombre: HotDog_obj}

    try:
        if response.status_code == 200:
            datos = response.json()
            cont_menu = 0
            for i in datos: # 'i' es un diccionario de un hotdog
                nombre_hotdog = i["nombre"]
                
                # --- MAPEO DE STRING A OBJETO ---
                # Busca los objetos de ingredientes usando el diccionario maestro
                pan_obj = _buscar_ingrediente_por_nombre(i["Pan"], dict_ingredientes)
                salchicha_obj = _buscar_ingrediente_por_nombre(i["Salchicha"], dict_ingredientes)
                acomp_obj = _buscar_ingrediente_por_nombre(i["Acompañante"], dict_ingredientes)
                
                # Para listas (toppings y salsas)
                salsas_key = "Salsas" if "Salsas" in i else "salsas"
                
                toppings_objs = [_buscar_ingrediente_por_nombre(t, dict_ingredientes) for t in i["toppings"]]
                salsas_objs = [_buscar_ingrediente_por_nombre(s, dict_ingredientes) for s in i[salsas_key]]
                
                # --- CREACIÓN DEL HOTDOG CON OBJETOS ---
                nuevo_hotdog = HotDog(nombre_hotdog, pan_obj, salchicha_obj, toppings_objs, salsas_objs, acomp_obj)
                
                # --- CORRECCIÓN DE GUARDADO ---
                # Guarda el hotdog usando su nombre como llave, no "combo"
                menu[nombre_hotdog] = nuevo_hotdog
                cont_menu += 1
                
            print(f"{cont_menu} combos cargados desde la API.")
            return menu
        
    except requests.exceptions.ConnectionError:
        print("Error de conexión: No se pudo acceder a la URL de GitHub.")
        return None
    except json.JSONDecodeError:
        print("Error de formato: El contenido de la URL no es un JSON válido.")
        return None

    

def cargar_datos_menu(archivo="menú.json"):
    """Carga los hotdogs agregados por el usuario desde el JSON local."""
    try:
        with open(archivo, 'rb') as a:
            return pickle.load(a)
    except Exception as e:
        return []


def guardar_datos_menu(menu, archivo="menú.json"):
    """Guarda los Hot Dogs locales en un archivo JSON."""
    try:
        with open(archivo, 'wb') as a:
            pickle.dump(menu, a)
    except Exception as e:
        print(f"Error al guardar el menú: {e}")
        return None





# Métodos de Gestión
"""def ver_lista_hotdogs(self):
    """
#Muestra la lista de Hot Dogs actualmente en el menú.
"""
    print("\n--- Menú Actual de Hot Dogs ---")
    if not self._menu_hotdogs:
        print("El menú está vacío.")
        return
    for nombre in self._menu_hotdogs.keys():
        print(f"- {nombre}")
def agregar_hotdog(self, hotdog, gestor_inventario):
    """
#Agrega un HotDog, realizando validaciones de longitud y existencia de inventario.
"""
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
    """
#Elimina un HotDog.
"""
    if nombre not in self._menu_hotdogs:
        return
    
    del self._menu_hotdogs[nombre]
    self.guardar_datos_locales()
    print(f"✅ HotDog '{nombre}' eliminado del menú.")"""
    
