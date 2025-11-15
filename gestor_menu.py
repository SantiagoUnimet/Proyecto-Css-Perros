from hotdogs import HotDog
import json
import requests
import pickle


# Métodos de Persistencia

def obtener_datos_menu():
    """Descarga y carga los datos iniciales de la API de GitHub."""
    
    api_menu = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"
    response = requests.get(api_menu)
    menu = {}

    try:
        if response.status_code == 200:
            datos = response.json()
            menu = {}
            cont_menu = 0
            for i in datos:
                for j in i:
                    if j == "Salsas":
                        nuevo_hotdog = HotDog(i["nombre"], i["Pan"], i["Salchicha"], i["toppings"], i[j], i["Acompañante"])
                    elif j == "salsas":
                        nuevo_hotdog = HotDog(i["nombre"], i["Pan"], i["Salchicha"], i["toppings"], i[j], i["Acompañante"])
                menu["combo"] = nuevo_hotdog
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
    
menu = cargar_datos_menu()

if not menu:
    print("No se encontró un menú cargado. Consultando a la API...")

    combo = obtener_datos_menu()
    if combo:
        menu.append(combo)
        guardar_datos_menu(menu)




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
    
